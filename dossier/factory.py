"""Fixed product install, explicit plan/apply, read-only status and finite rollback."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from . import runtime
from .paths import SOURCE_ROOT
from .release import git, snapshot, ReleaseError, remove_created
from .install import build_structure, collect_manifest, render

_spec = importlib.util.spec_from_file_location('dossier_bootstrap', SOURCE_ROOT / 'bootstrap.py')
bootstrap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bootstrap)


def create_file(host, rel, data, created):
    """Publish a complete new file exclusively; register identity before linking.

    The temporary inode lives on the target filesystem. link() atomically fails
    if a target appeared after preflight, unlike replace() which would clobber
    it. An interrupted temporary write never exposes a partial target.
    """
    target = runtime.safe(host, rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.dossier-create-' + target.name + '-', dir=target.parent)
    temp = Path(name)
    os.close(fd)
    try:
        temp.write_bytes(data)
        info = temp.stat()
        created[rel] = (info.st_dev, info.st_ino, runtime.digest(data))
        os.link(temp, target)
    finally:
        temp.unlink()


def remove_created_files(host, created):
    """Remove only our published inode while its bytes still match."""
    for rel, (device, inode, expected) in created.items():
        try:
            path = runtime.safe(host, rel)
            info = path.stat()
            if (info.st_dev, info.st_ino) == (device, inode) and runtime.digest(runtime.read(host, rel)) == expected:
                path.unlink()
        except (FileNotFoundError, runtime.RuntimeError):
            # A removed/replaced path or new symlink is no longer ours. Do not
            # follow it or prevent restoration of the remaining transaction.
            continue


def prepare(repository, version, directory, host):
    commit = bootstrap.obtain(repository, version, directory)
    snap = snapshot(directory, commit, product=True)
    dep = host / runtime.DEPENDENCY
    if (dep / '.git').is_file():
        old = git(dep, 'rev-parse', 'HEAD').decode().strip()
        git(directory, 'fetch', '--no-tags', str(dep), old)
    return commit, snap


def plan(repository, host_root, version=None):
    host = Path(host_root).resolve()
    repository, version = bootstrap.select(repository, version)
    with tempfile.TemporaryDirectory(prefix='dossier-factory-') as tmp:
        repo = Path(tmp) / 'product'
        commit, snap = prepare(repository, version, repo, host)
        value = runtime.plan(repo, commit, host, product=True, canonical=repository)
        value['selection'] = dict(repository=repository, tag=version, product_commit=commit, tree=snap['tree'])
        return value


def apply(plan, host_root=None):
    value = json.loads(Path(plan).read_text(encoding='utf-8')) if isinstance(plan, (str, Path)) else plan
    value = dict(value)
    selected = value.pop('selection')
    if selected != dict(repository=value['repository'], tag=selected['tag'], product_commit=value['source_commit'], tree=value['target_tree']):
        raise ValueError('Plan selection mismatch')
    host = Path(host_root or value['host']).resolve()
    with tempfile.TemporaryDirectory(prefix='dossier-factory-') as tmp:
        repo = Path(tmp) / 'product'
        commit, _ = prepare(selected['repository'], selected['product_commit'], repo, host)
        if commit != selected['product_commit']: raise ValueError('Product changed')
        return runtime.apply(repo, None, value, host)


def install(repository, host_root, version=None):
    host = Path(host_root).resolve()
    if (host / runtime.DEPENDENCY).exists() or (host / runtime.STATE).exists():
        result = runtime.status(host)
        if not result['ok'] or not result['registered']: raise ValueError('Existing installation cannot be adopted by install')
        if version:
            head = result['product_commit']
            dep = host / runtime.DEPENDENCY
            fixed = git(dep, 'rev-parse', '--verify', '--end-of-options', version + '^{commit}', check=False).decode().strip()
            if fixed != head: raise ValueError('Already installed; use factory plan/apply to upgrade')
        return dict(**result, idempotent=True)
    if Path(git(host, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != host:
        raise ValueError('Host must be its Git repository root')
    repository, version = bootstrap.select(repository, version)
    with tempfile.TemporaryDirectory(prefix='dossier-factory-') as tmp:
        product = Path(tmp) / 'product'
        commit, snap = prepare(repository, version, product, host)
        # The caller must itself be the selected installer, including its templates.
        if git(SOURCE_ROOT, 'rev-parse', 'HEAD', check=False).decode().strip() != commit:
            returncode = subprocess.call([sys.executable, '-B', str(product / 'dossier.py'), 'factory', 'install',
                                          '--repository', repository, '--version', commit, '--host-root', str(host)])
            if returncode: raise ValueError('Selected installer failed')
            return dict(phase='installed', product_commit=commit)
        files = {}
        for rel, content in build_structure():
            if content is not None: files[rel] = render(content, runtime.DEPENDENCY).encode()
        for rel in collect_manifest(product):
            template = product / 'templates' / rel
            if template.is_file(): files[rel] = render(template.read_text(encoding='utf-8'), runtime.DEPENDENCY).encode()
        files[runtime.BASELINE] = None
        files[runtime.STATE] = None
        for rel in files:
            if runtime.safe(host, rel).exists(): raise ValueError('Existing installation target: ' + rel)
        runtime.dependency(host, False)
        directories = {parent for rel in [*files, runtime.DEPENDENCY] for parent in runtime.safe(host, rel).parents if parent != host and parent.is_relative_to(host)}
        before_dirs = {p for p in directories if p.exists()}
        record = dict(dependency=dict(head=None), files={'.gitmodules': runtime.encode(runtime.read(host, '.gitmodules'))},
                      index=git(host, 'ls-files', '--stage', '--', runtime.DEPENDENCY, '.gitmodules').decode(),
                      managed_before=git(host, 'config', '--get', 'dossier.runtime.managed', check=False).decode().strip(), created_metadata=True)
        created = {}
        try:
            dep = runtime.safe(host, runtime.DEPENDENCY)
            metadata = Path(git(host, 'rev-parse', '--absolute-git-dir').decode().strip()) / 'modules/dossier-runtime'
            metadata.parent.mkdir(parents=True, exist_ok=True)
            git(host, 'clone', '--no-hardlinks', '--separate-git-dir=' + str(metadata), str(product), str(dep))
            git(dep, 'remote', 'set-url', 'origin', repository)
            git(host, 'config', '-f', '.gitmodules', 'submodule.dossier-runtime.path', runtime.DEPENDENCY)
            git(host, 'config', '-f', '.gitmodules', 'submodule.dossier-runtime.url', repository)
            git(host, 'config', 'submodule.dossier-runtime.url', repository)
            git(host, 'update-index', '--add', '--cacheinfo', '160000,' + commit + ',' + runtime.DEPENDENCY)
            for rel, data in files.items():
                if data is not None:
                    create_file(host, rel, data, created)
            from .install import write_baseline
            writer = lambda rel, data: create_file(host, rel, data, created)
            if write_baseline(host, dep, writer=writer) is None: raise ValueError('Baseline creation failed')
            managed = {rel: runtime.digest(runtime.read(host, rel)) for rel in runtime.templates(product, snap['tree'], runtime.DEPENDENCY)}
            state = dict(version=1, host=str(host), phase='active', product_commit=commit,
                         source_commit=commit, target_tree=snap['tree'], registration_url=repository, files=managed)
            writer(runtime.STATE, (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
            git(host, 'config', 'dossier.runtime.managed', 'true')
            runtime.validate(host, dict(files=[dict(path=p) for p in managed]), dep)
            return dict(phase='active', product_commit=commit, review=[runtime.DEPENDENCY, '.gitmodules', *files], message='Review changes; load rules in the next session')
        except Exception:
            remove_created_files(host, created)
            runtime.restore(host, record)
            for p in sorted(directories, key=lambda p: len(p.parts), reverse=True):
                if p not in before_dirs:
                    try: p.rmdir()
                    except OSError: pass
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('install', 'plan', 'apply', 'status', 'rollback'):
        p = sub.add_parser(name); p.add_argument('--host-root', required=True)
        if name in ('install', 'plan'):
            p.add_argument('--repository', required=True); p.add_argument('--version', help='Fixed tag or commit; otherwise GitHub latest formal Release or highest Codeup formal vX.Y.Z tag')
        if name == 'apply': p.add_argument('--plan', required=True)
    args = vars(parser.parse_args(argv)); command = args.pop('command')
    try:
        result = getattr(runtime, command)(**args) if command in ('status', 'rollback') else globals()[command](**args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if command == 'status' and not result['ok'] else 0
    except (ReleaseError, OSError, ValueError, KeyError) as exc:
        print('factory: ' + str(exc), file=sys.stderr); return 1
