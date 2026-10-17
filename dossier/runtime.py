"""Plan and transact a local, explicitly published runtime upgrade.

adopt-source syntax: REF:src@OLD_PREFIX or REF:.@OLD_PREFIX. The former
selects a development commit, the latter a product commit. No remote lookup.
"""
import argparse
import base64
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

from .install import render
from .release import git, repository, snapshot, ReleaseError, git_environment, remove_created

DEPENDENCY = 'submodules/dossier'
STATE = '.dossier/runtime.json'
BACKUP = '.dossier/upgrade-backup/record.json'
BASELINE = '.dossier/baseline.json'

class RuntimeError(ReleaseError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None

def safe(host, rel):
    parts = PurePosixPath(rel).parts
    if not parts or any(x in ('..', '.', '') or ':' in x or '\\' in x for x in parts) or rel.startswith('/'):
        raise RuntimeError('Unsafe path: ' + rel)
    p = host
    for part in parts:
        p = p / part
        if p.is_symlink():
            raise RuntimeError('Symbolic link: ' + rel)
    if not p.resolve().is_relative_to(host.resolve()):
        raise RuntimeError('Path outside host: ' + rel)
    return p

def read(host, rel):
    p = safe(host, rel)
    if p.exists() and not p.is_file():
        raise RuntimeError('Expected file: ' + rel)
    return p.read_bytes() if p.exists() else None

def load(host):
    raw = read(host, STATE)
    if raw is None:
        return None
    value = json.loads(raw)
    if value.get('version') != 1 or value.get('host') != str(host):
        raise RuntimeError('Runtime record does not match host')
    return value

def save(host, rel, value):
    path = safe(host, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Durable records must never become partially written JSON.
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.runtime-', delete=False) as stream:
        temp = Path(stream.name)
        stream.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())
    try: os.replace(temp, path)
    finally:
        if temp.exists(): temp.unlink()

def write(host, rel, data):
    path = safe(host, rel)
    if data is None:
        if path.exists(): path.unlink()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

def encode(data):
    return None if data is None else base64.b64encode(data).decode('ascii')

def decode(data):
    return None if data is None else base64.b64decode(data, validate=True)

def templates(repo, tree, prefix):
    result = {}
    for raw in git(repo, 'ls-tree', '-rz', tree, '--', 'templates').split(b'\0'):
        if not raw: continue
        meta, path = raw.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        rel = path.decode().removeprefix('templates/')
        if mode not in ('100644', '100755') or kind != 'blob':
            raise RuntimeError('Unsupported template: ' + rel)
        if not (rel in ('CLAUDE.md', 'AGENTS.md') or rel.startswith(('.claude/', '.codex/', '.cursor/', '.agents/skills/'))):
            raise RuntimeError('Template outside execution scope: ' + rel)
        if rel.endswith('settings.local.json'):
            raise RuntimeError('Private template')
        result[rel] = render(git(repo, 'cat-file', 'blob', oid).decode('utf-8'), prefix)
    return result

def source(repo, value):
    try:
        location, prefix = value.rsplit('@', 1)
        ref, subtree = location.rsplit(':', 1)
    except ValueError:
        raise RuntimeError('adopt-source must be REF:src@OLD_PREFIX or REF:.@OLD_PREFIX')
    if subtree not in ('src', '.') or not prefix or prefix == DEPENDENCY:
        raise RuntimeError('Explicit old source and distinct prefix required')
    commit = git(repo, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
    tree = git(repo, 'rev-parse', commit + (':src' if subtree == 'src' else '^{tree}')).decode().strip()
    return dict(commit=commit, tree=tree, prefix=prefix)

def ordinary(host):
    """Verify an unmanaged, fixed product submodule without creating records."""
    if git(host, 'config', '--get', 'dossier.runtime.managed', check=False).strip(): return None
    rows = git(host, 'config', '-f', '.gitmodules', '--get-regexp', '^submodule\\..*\\.path$', check=False).decode().splitlines()
    matches = [row.split(None, 1)[0][len('submodule.'):-len('.path')]
               for row in rows if len(row.split(None, 1)) == 2 and row.split(None, 1)[1] == DEPENDENCY]
    if not matches or matches == ['dossier-runtime']: return None
    if len(matches) != 1: raise RuntimeError('Ambiguous product submodule registration')
    section = matches[0]
    p = safe(host, DEPENDENCY)
    if not (p / '.git').is_file(): raise RuntimeError('Ordinary dependency is not a standard submodule')
    urls = git(host, 'config', '-f', '.gitmodules', '--get-all', 'submodule.' + section + '.url', check=False).decode().splitlines()
    origin = git(p, 'config', '--get', 'remote.origin.url', check=False).decode().strip()
    if len(urls) != 1 or not origin or origin != urls[0]: raise RuntimeError('Ordinary dependency source mismatch')
    head = git(p, 'rev-parse', 'HEAD').decode().strip()
    index = git(host, 'ls-files', '--stage', '--', DEPENDENCY).decode().strip()
    if not index.startswith('160000 ' + head + ' 0\t') or git(p, 'status', '--porcelain').strip():
        raise RuntimeError('Ordinary dependency HEAD/Gitlink mismatch or dirty checkout')
    snapshot(p, head, product=True)
    baseline = json.loads(read(host, BASELINE) or b'null')
    if not baseline or baseline.get('parent_head') != head or not isinstance(baseline.get('files'), dict):
        raise RuntimeError('Ordinary dependency baseline missing or source mismatch')
    from .install import collect_manifest
    if not set(collect_manifest(p)).issubset(baseline['files']): raise RuntimeError('Ordinary dependency baseline incomplete')
    return dict(head=head, index=index, section=section, url=origin)

def dependency(host, registered=False):
    p = safe(host, DEPENDENCY)
    index = git(host, 'ls-files', '--stage', '--', DEPENDENCY).decode().strip()
    if not p.exists():
        if registered or index: raise RuntimeError('Registered dependency missing')
        gitdir = Path(git(host, 'rev-parse', '--absolute-git-dir').decode().strip()) / 'modules/dossier-runtime'
        if gitdir.exists(): raise RuntimeError('Unknown existing submodule metadata')
        if git(host, 'config', '-f', '.gitmodules', '--get-regexp', '^submodule\\.dossier-runtime\\.', check=False).strip():
            raise RuntimeError('Unknown existing submodule registration')
        return dict(head=None, index=index)
    if not registered:
        raise RuntimeError('Unknown existing dependency directory')
    if not (p / '.git').is_file(): raise RuntimeError('Dependency is not a standard submodule')
    state = load(host)
    section = (state or {}).get('registration_section', 'dossier-runtime')
    registered_path = git(host, 'config', '-f', '.gitmodules', '--get-all', 'submodule.' + section + '.path', check=False).decode().splitlines()
    registered_url = git(host, 'config', '-f', '.gitmodules', '--get-all', 'submodule.' + section + '.url', check=False).decode().splitlines()
    expected_url = (state or {}).get('registration_url')
    origin_url = git(p, 'config', '--get', 'remote.origin.url', check=False).decode().strip()
    if registered_path != [DEPENDENCY] or not expected_url or registered_url != [expected_url] or origin_url != expected_url:
        raise RuntimeError('Dependency registration path/source mismatch')
    head = git(p, 'rev-parse', 'HEAD').decode().strip()
    if not index.startswith('160000 ' + head + ' 0\t'):
        raise RuntimeError('Dependency HEAD/Gitlink mismatch')
    if git(p, 'status', '--porcelain').strip(): raise RuntimeError('Dirty dependency')
    return dict(head=head, index=index)

def merge(current, base, target):
    if current == base: return target, None
    if current == target or base == target: return current, None
    if base is None: return None, 'new file already exists'
    if current is None: return None, 'managed file missing'
    if target is None: return None, 'retired file has customization'
    with tempfile.TemporaryDirectory(prefix='dossier-merge-') as tmp:
        paths = [Path(tmp) / x for x in ('current', 'base', 'target')]
        for p, text in zip(paths, (current, base, target)): p.write_text(text, encoding='utf-8', newline='\n')
        proc = subprocess.run(['git', 'merge-file', '-p', *map(str, paths)], capture_output=True, env=git_environment())
        if proc.returncode: return None, 'three-way text conflict'
        return proc.stdout.decode('utf-8'), None

def plan(repo=None, ref='HEAD', host_root=None, adopt_source=None, product=False, canonical=None):
    repo = Path(repo or repository()).resolve()
    if host_root is None: raise RuntimeError('Explicit host-root required')
    host = Path(host_root).resolve()
    if Path(git(host, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != host:
        raise RuntimeError('Host must be its repository root')
    state = load(host)
    if state and state.get('phase') != 'active': raise RuntimeError('Runtime requires recovery before a new plan')
    if state:
        checked = status(host)
        if not checked['ok']: raise RuntimeError('Active runtime drift: ' + ', '.join(checked['problems']))
        old = dict(commit=state['product_commit'], tree=state['target_tree'], prefix=DEPENDENCY)
    elif ordinary(host):
        dep = host / DEPENDENCY
        head = git(dep, 'rev-parse', 'HEAD').decode().strip()
        git(repo, 'fetch', '--no-tags', str(dep), head)
        old = dict(commit=head, tree=snapshot(repo, head, product=True)['tree'], prefix=DEPENDENCY)
    elif adopt_source:
        old = source(repo, adopt_source)
    else:
        raise RuntimeError('First registration requires explicit --adopt-source')
    snap = snapshot(repo, ref, product=product)
    previous = templates(repo, old['tree'], DEPENDENCY)
    old_templates = templates(repo, old['tree'], '{{DOSSIER_ROOT}}')
    target = templates(repo, snap['tree'], DEPENDENCY)
    before = dependency(host, True) if state else (ordinary(host) or dependency(host, False))
    paths = set(previous) | set(target)
    # Extra host-owned role/skill files also need explicit old-prefix wiring.
    for folder in ('.claude/agents', '.claude/skills', '.codex/agents', '.codex/skills'):
        root = safe(host, folder)
        if root.exists():
            for p in root.rglob('*'):
                if p.is_symlink(): raise RuntimeError('Symbolic role/skill path')
                if p.is_file(): paths.add(p.relative_to(host).as_posix())
    entries = []; conflicts = []
    for rel in sorted(paths):
        raw = read(host, rel)
        current = raw.decode('utf-8') if raw is not None else None
        if rel not in previous and rel not in target:
            candidate, conflict = current, None
            if current is not None and old['prefix'] != DEPENDENCY:
                # Extra host-owned files have no template base. Only exact,
                # verifiable rule references are safe to wire automatically.
                pattern = r'(?<![\w./-])' + re.escape(old['prefix']) + r'/rules/([\w./-]*)'
                def wire(match):
                    nonlocal conflict
                    tail = match.group(1)
                    if not tail.endswith('.md'):
                        return match.group(0)
                    path = 'rules/' + tail
                    if '..' in PurePosixPath(path).parts or not git(repo, 'cat-file', '-t', old['tree'] + ':' + path.rstrip('/'), check=False).strip():
                        conflict = 'unverifiable old source pointer'
                        return match.group(0)
                    return DEPENDENCY + '/' + path
                candidate = re.sub(pattern, wire, current)
                for suffix in ('/dossier.py', '/tools/', '/tests/'):
                    if old['prefix'] + suffix in candidate:
                        conflict = 'host-owned runtime pointer needs explicit review'
        else:
            normalized = current
            if current is not None and old['prefix'] != DEPENDENCY:
                # Normalize only the exact source references declared by this
                # old template's placeholders. Generic src/* permission text
                # is not a template source reference and stays byte-for-byte.
                suffixes = set(re.findall(r'\{\{DOSSIER_ROOT\}\}(/[\w./-]*)', old_templates.get(rel, '')))
                # A bare directory is also a common business permission range.
                # Only migrate it when the complete original template line is
                # present, so a host's "do not write src/rules/" stays intact.
                for line in old_templates.get(rel, '').splitlines():
                    if any('{{DOSSIER_ROOT}}' + suffix in line for suffix in suffixes if suffix.endswith('/')):
                        normalized = normalized.replace(render(line, old['prefix']), render(line, DEPENDENCY))
                for suffix in sorted(suffixes, key=len, reverse=True):
                    if suffix.endswith('/'):
                        continue
                    pointer = old['prefix'] + suffix
                    normalized = re.sub(r'(?<![\w./-])' + re.escape(pointer) + r'(?![\w./*-])',
                                        lambda match: DEPENDENCY + suffix, normalized)
            candidate, conflict = merge(normalized, previous.get(rel), target.get(rel))
        if candidate is not None and not conflict:
            if '{{DOSSIER_ROOT}}' in candidate:
                conflict = 'unresolved source pointer'
            # File references identify a rule source. Bare rules/ directories
            # and rules/* permission ranges do not establish source identity.
            for match in re.finditer(r'(?<![\w./-])((?:\.{1,2}/|[\w.-]+/)+)rules/[\w.-]+\.md(?![\w./-])', candidate):
                if match.group(1).rstrip('/') not in (DEPENDENCY, '.cursor'):
                    conflict = 'unknown source pointer prefix: ' + match.group(1)
            if rel.endswith('.json'):
                try: json.loads(candidate)
                except ValueError: conflict = 'candidate JSON is invalid'
        if conflict: conflicts.append(dict(path=rel, reason=conflict))
        action = 'conflict' if conflict else 'keep' if candidate == current else 'delete' if candidate is None else 'write'
        entries.append(dict(path=rel, before=digest(raw), action=action,
                            content=candidate if action == 'write' else None))
    result = dict(version=1, host=str(host), repository=canonical or str(repo), source_commit=snap['commit'],
                target_tree=snap['tree'], old_source=old, dependency=before,
                registration_before=digest(read(host, '.gitmodules')),
                state_before=digest(read(host, STATE)), baseline_before=digest(read(host, BASELINE)),
                files=entries, conflicts=conflicts,
                registration=dict(path=DEPENDENCY, url=(state or {}).get('registration_url') or (ordinary(host) or {}).get('url') or canonical or str(repo)),
                assumption='Old templates are a comparison base, not proof of prior generation')
    if product: result['product_target'] = True
    return result

def published(repo, tag):
    ref = 'refs/tags/' + tag
    if git(repo, 'cat-file', '-t', ref).strip() != b'tag': raise RuntimeError('Annotated product tag required')
    commit = git(repo, 'rev-parse', ref + '^{commit}').decode().strip()
    msg = git(repo, 'show', '-s', '--format=%B', commit).decode()
    if not msg.startswith('Dossier product\n\nSource-commit: '): raise RuntimeError('Not a published product')
    origin = msg.split('Source-commit: ', 1)[1].splitlines()[0]
    tree = git(repo, 'rev-parse', commit + '^{tree}').decode().strip()
    if '\nProduct-tree: ' + tree not in msg: raise RuntimeError('Product provenance mismatch')
    snapshot(repo, commit, product=True)
    if git(repo, 'cat-file', '-t', origin, check=False).strip() == b'commit' and snapshot(repo, origin)['tree'] != tree:
        raise RuntimeError('Product/source tree mismatch')
    return commit, origin, tree

def check_plan(host, value):
    if value.get('version') != 1 or value.get('host') != str(host): raise RuntimeError('Plan host/version mismatch')
    if value['conflicts']: raise RuntimeError('Plan has conflicts')
    for rel, key in (('.gitmodules', 'registration_before'), (STATE, 'state_before'), (BASELINE, 'baseline_before')):
        if digest(read(host, rel)) != value[key]: raise RuntimeError('Stale plan: ' + rel)
    actual = dependency(host, True) if load(host) else (ordinary(host) or dependency(host, False))
    if actual != value['dependency']: raise RuntimeError('Stale dependency')
    for item in value['files']:
        if digest(read(host, item['path'])) != item['before']: raise RuntimeError('Stale plan: ' + item['path'])

def validate(host, value, product):
    for item in value['files']:
        raw = read(host, item['path'])
        if raw is not None and item['path'].endswith('.json'): json.loads(raw)
    probe = subprocess.run([os.sys.executable, '-B', '-X', 'utf8', str(product / 'dossier.py'), 'setup-probe', str(host)],
                           capture_output=True, env=git_environment())
    if probe.returncode: raise RuntimeError('Runtime startup probe failed: ' + probe.stdout.decode('utf-8', 'replace')[-2000:])
    bash = str(Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Git/bin/bash.exe') if os.name == 'nt' else shutil.which('bash')
    if not bash: raise RuntimeError('Git Bash is required for the runtime environment check')
    environment = subprocess.run([bash, str(product / 'checks/check-env.sh'), '--host-root', str(host)],
                                 cwd=host, capture_output=True, env=git_environment())
    if environment.returncode:
        raise RuntimeError('Runtime environment check failed: ' + (environment.stdout + environment.stderr).decode('utf-8', 'replace')[-2000:])

def restore(host, record):
    p = safe(host, DEPENDENCY)
    if record['dependency']['head']:
        git(p, 'checkout', '--detach', record['dependency']['head'])
    elif record.get('created_metadata') and p.exists():
        # Only our previously verified, freshly created checkout is removed.
        remove_created(p)
    for rel, data in record['files'].items(): write(host, rel, decode(data))
    index = record['index']
    for rel in (DEPENDENCY, '.gitmodules'):
        git(host, 'update-index', '--force-remove', '--', rel)
    if index: git(host, 'update-index', '--index-info', data=index.encode())
    if 'managed_before' in record:
        if record['managed_before']: git(host, 'config', 'dossier.runtime.managed', record['managed_before'])
        else: git(host, 'config', '--unset-all', 'dossier.runtime.managed', check=False)
    if not record['dependency']['head']:
        git(host, 'config', '--remove-section', 'submodule.dossier-runtime', check=False)
        gitdir = Path(git(host, 'rev-parse', '--absolute-git-dir').decode().strip()) / 'modules/dossier-runtime'
        if record.get('created_metadata') and gitdir.exists(): remove_created(gitdir)

def apply(repo=None, tag=None, plan=None, host_root=None):
    value = json.loads(Path(plan).read_text(encoding='utf-8')) if isinstance(plan, (str, Path)) else plan
    if not isinstance(value, dict): raise RuntimeError('Plan required')
    host = Path(host_root or value['host']).resolve(); repo = Path(repo or value['repository']).resolve()
    if value.get('product_target'):
        commit = value['source_commit']
        fixed = snapshot(repo, commit, product=True)
        origin, tree = commit, fixed['tree']
        if tag and git(repo, 'rev-parse', '--verify', '--end-of-options', tag + '^{commit}').decode().strip() != commit:
            raise RuntimeError('Selected tag moved')
    else:
        commit, origin, tree = published(repo, tag)
    if (origin, tree) != (value['source_commit'], value['target_tree']): raise RuntimeError('Tag does not match planned candidate')
    state = load(host)
    if state and state.get('phase') == 'active' and state.get('product_commit') == commit:
        result = status(host)
        if result['ok']: return dict(phase='active', product_commit=commit, idempotent=True)
        raise RuntimeError('Applied runtime has drift')
    if state and state.get('phase') == 'needs-recovery': raise RuntimeError('Manual recovery required')
    check_plan(host, value)
    old = value['old_source']
    options = dict(product=bool(value.get('product_target')), canonical=value['repository'])
    if state or ordinary(host):
        rebuilt = globals()['plan'](repo, origin, host, **options)
    else:
        # The original selector is fixed by its resolved commit/tree, never a mutable ref.
        root_tree = git(repo, 'rev-parse', old['commit'] + '^{tree}').decode().strip()
        selector = old['commit'] + (':.@' if root_tree == old['tree'] else ':src@') + old['prefix']
        rebuilt = globals()['plan'](repo, origin, host, selector, **options)
    if value != rebuilt: raise RuntimeError('Plan differs from independently recomputed plan')
    affected = [x['path'] for x in value['files']] + ['.gitmodules', BASELINE, STATE]
    record = dict(version=1, host=str(host), dependency=value['dependency'],
                  managed_before=git(host, 'config', '--get', 'dossier.runtime.managed', check=False).decode().strip(),
                  index=git(host, 'ls-files', '--stage', '--', DEPENDENCY, '.gitmodules').decode(),
                  files={rel: encode(read(host, rel)) for rel in affected},
                  previous_backup=encode(read(host, BACKUP)))
    save(host, BACKUP, record)
    transaction = dict(version=1, host=str(host), phase='applying', product_commit=commit,
                       source_commit=origin, target_tree=tree,
                       registration_url=value['registration']['url'],
                       registration_section=(state or {}).get('registration_section') or value['dependency'].get('section', 'dossier-runtime'))
    try:
        save(host, STATE, transaction)
        git(host, 'config', 'dossier.runtime.managed', 'true')
        dep = safe(host, DEPENDENCY)
        if not dep.exists():
            dep.parent.mkdir(parents=True, exist_ok=True)
            # A normal submodule gitfile, without network or touching other index entries.
            gitdir = Path(git(host, 'rev-parse', '--absolute-git-dir').decode().strip()) / 'modules/dossier-runtime'
            if gitdir.exists(): raise RuntimeError('Existing submodule metadata requires recovery')
            gitdir.parent.mkdir(parents=True, exist_ok=True)
            record['created_metadata'] = True
            save(host, BACKUP, record)
            git(host, 'clone', '--no-checkout', '--no-hardlinks', '--separate-git-dir=' + str(gitdir), str(repo), str(dep))
            git(host, 'config', '-f', '.gitmodules', 'submodule.dossier-runtime.path', DEPENDENCY)
            git(host, 'config', '-f', '.gitmodules', 'submodule.dossier-runtime.url', transaction['registration_url'])
            git(host, 'config', 'submodule.dossier-runtime.url', transaction['registration_url'])
            git(dep, 'remote', 'set-url', 'origin', transaction['registration_url'])
        else:
            git(dep, 'fetch', '--no-tags', str(repo), commit)
        git(dep, 'checkout', '--detach', commit)
        git(host, 'update-index', '--add', '--cacheinfo', '160000,' + commit + ',' + DEPENDENCY)
        for item in value['files']:
            if item['action'] == 'write': write(host, item['path'], item['content'].encode('utf-8'))
            elif item['action'] == 'delete': write(host, item['path'], None)
        validate(host, value, dep)
        files = {x['path']: digest(read(host, x['path'])) for x in value['files']}
        baseline = dict(version=1, generated_at=datetime.now(timezone.utc).isoformat(), parent_head=commit,
                        hash_algorithm='git-blob-sha1', files={})
        for rel in files:
            raw = read(host, rel)
            if raw is not None: baseline['files'][rel] = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
        save(host, BASELINE, baseline)
        transaction.update(phase='active', files=files, tag=tag)
        save(host, STATE, transaction)
        record['after'] = {rel: digest(read(host, rel)) for rel in affected}
        record['after_dependency'] = dependency(host, True)
        # Only the newest completed recovery point survives success. The
        # previous completed point is retained solely during this transaction.
        completed = {key: item for key, item in record.items() if key != 'previous_backup'}
        save(host, BACKUP, completed)
        return dict(phase='active', product_commit=commit, review=[DEPENDENCY, '.gitmodules', *files],
                    message='Review host changes; load updated rules in the next session')
    except Exception as exc:
        try:
            restore(host, record)
            write(host, BACKUP, decode(record['previous_backup']))
        except Exception as recovery:
            transaction.update(phase='needs-recovery', error=str(exc), recovery_error=str(recovery))
            save(host, STATE, transaction)
            raise RuntimeError('Update failed; needs-recovery: ' + str(recovery)) from exc
        raise RuntimeError('Update failed; previous runtime restored: ' + str(exc)) from exc

def status(host_root):
    host = Path(host_root).resolve(); state = load(host)
    if not state:
        registration = git(host, 'config', '-f', '.gitmodules', '--get-regexp', '^submodule\\..*\\.path$', check=False).decode()
        top = git(host, 'rev-parse', '--show-toplevel', check=False).decode().strip()
        own_repository = bool(top and Path(top).resolve() == host)
        linked = git(host, 'ls-files', '--stage', '--', DEPENDENCY).strip() if own_repository else b''
        gitdir_raw = git(host, 'rev-parse', '--absolute-git-dir', check=False).decode().strip() if own_repository else ''
        metadata = bool(gitdir_raw and (Path(gitdir_raw) / 'modules/dossier-runtime').exists())
        try:
            fixed = ordinary(host) if linked and not metadata else None
        except (ReleaseError, OSError, ValueError) as exc:
            return dict(phase='needs-recovery', ok=False, registered=True, source=str(host / DEPENDENCY), problems=[str(exc)])
        if fixed:
            return dict(phase='fixed', ok=True, registered=True, source=str(host / DEPENDENCY), product_commit=fixed['head'], problems=[])
        if linked or any(line.split(None, 1)[-1] == DEPENDENCY for line in registration.splitlines()) or metadata or git(host, 'config', '--get', 'dossier.runtime.managed', check=False).strip():
            return dict(phase='needs-recovery', ok=False, registered=True, source=str(host / DEPENDENCY),
                        problems=['Runtime record missing while dependency registration remains'])
        return dict(phase='unregistered', ok=True, registered=False, source=None,
                    message='Not decoupled; legacy source checks apply')
    problems = []
    if state.get('phase') != 'active': problems.append('runtime phase is ' + str(state.get('phase')))
    try:
        dep = dependency(host, True)
        if dep['head'] != state.get('product_commit'): problems.append('dependency version mismatch')
        actual_tree = git(host / DEPENDENCY, 'rev-parse', 'HEAD^{tree}').decode().strip()
        if actual_tree != state.get('target_tree'): problems.append('dependency tree mismatch')
    except ReleaseError as exc: problems.append(str(exc))
    for rel, expected in state.get('files', {}).items():
        if digest(read(host, rel)) != expected: problems.append('drift: ' + rel)
    return dict(phase=state.get('phase'), ok=not problems, registered=True,
                source=str(host / DEPENDENCY), product_commit=state.get('product_commit'), problems=problems)

def rollback(host_root):
    host = Path(host_root).resolve()
    record = json.loads(read(host, BACKUP) or b'null')
    if not record or 'after' not in record: raise RuntimeError('No completed upgrade to roll back')
    if dependency(host, True) != record['after_dependency']: raise RuntimeError('Dependency changed after upgrade')
    for rel, expected in record['after'].items():
        if digest(read(host, rel)) != expected: raise RuntimeError('Changed after upgrade: ' + rel)
    try: restore(host, record)
    except Exception as exc:
        state = load(host) or dict(version=1, host=str(host))
        state.update(phase='needs-recovery', error=str(exc)); save(host, STATE, state)
        raise
    write(host, BACKUP, None)
    return dict(phase='rolled-back', message='Load restored rules in the next session')

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('plan', 'apply', 'status', 'rollback'):
        p = sub.add_parser(name); p.add_argument('--host-root', required=True)
        if name == 'plan':
            p.add_argument('--ref', default='HEAD'); p.add_argument('--adopt-source', help='REF:src@OLD_PREFIX or REF:.@OLD_PREFIX')
        if name == 'apply': p.add_argument('--tag', required=True); p.add_argument('--plan', required=True)
    args = vars(parser.parse_args(argv)); command = args.pop('command')
    try:
        result = globals()[command](**args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if command == 'status' and not result['ok'] else 0
    except (ReleaseError, OSError, ValueError, KeyError) as exc:
        print('runtime: ' + str(exc), file=os.sys.stderr); return 1
