"""Export a fixed committed product subtree and publish local references atomically."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

class ReleaseError(RuntimeError):
    pass

def git_environment():
    # Hooks and parent Git invocations may export repository/index overrides.
    local = {'GIT_DIR','GIT_COMMON_DIR','GIT_WORK_TREE','GIT_INDEX_FILE',
             'GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES',
             'GIT_GRAFT_FILE','GIT_NAMESPACE','GIT_PREFIX','GIT_SUPER_PREFIX',
             'GIT_IMPLICIT_WORK_TREE','GIT_CONFIG','GIT_CONFIG_PARAMETERS','GIT_CONFIG_COUNT'}
    return {k:v for k,v in os.environ.items() if k not in local and not k.startswith(('GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_'))}

def git(repo, *args, data=None, check=True):
    p = subprocess.run(['git', '-C', str(repo), *args], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_environment())
    if check and p.returncode:
        raise ReleaseError(p.stderr.decode('utf-8', 'replace').strip() or 'Git command failed')
    return p.stdout

def repository():
    return Path(git(Path(__file__).parent, 'rev-parse', '--show-toplevel').decode().strip())

def snapshot(repo, ref, product=False):
    commit = git(repo, 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()
    tree = git(repo, 'rev-parse', '--verify', commit + ('^{tree}' if product else ':src')).decode().strip()
    if git(repo, 'cat-file', '-t', tree).strip() != b'tree':
        raise ReleaseError('src must be a tree')
    entries = []
    seen = set()
    forbidden = {'.git', '.mail', '.dossier', '.venv', '.tmp', '.zwork', '__pycache__', 'node_modules'}
    for line in git(repo, 'ls-tree', '-rz', '--full-tree', tree).split(b'\0'):
        if not line: continue
        meta, raw = line.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = raw.decode('utf-8')
        parts = PurePosixPath(name).parts
        folded = name.casefold()
        if folded in seen:
            raise ReleaseError('Case-colliding product path: ' + name)
        seen.add(folded)
        if mode not in ('100644', '100755') or kind != 'blob':
            raise ReleaseError('Unsupported product mode: ' + name)
        if not parts or any(p in ('', '.', '..') or ':' in p or '\\' in p for p in parts) or name.startswith('/'):
            raise ReleaseError('Unsafe product path: ' + name)
        if any(p.lower() in forbidden or p.lower().startswith('.env') or p.lower().endswith(('.pyc', '.pyo')) or p.lower().endswith(('.pem', '.key', '.p12', '.pfx')) or p.lower() in ('settings.local.json', 'credentials.json', 'id_rsa', 'id_ed25519', 'todo.md', 'session.md') for p in parts):
            raise ReleaseError('Private/development material in src: ' + name)
        if parts[0] == 'docs':
            raise ReleaseError('Development docs in src: ' + name)
        if parts[0].casefold() == 'examples' or tuple(p.casefold() for p in parts[:2]) == ('tools', 'figures'):
            raise ReleaseError('Development figure tools in src: ' + name)
        if parts[0] == 'tests':
            raise ReleaseError('Development tests in src: ' + name)
        size = int(git(repo, 'cat-file', '-s', oid))
        entries.append(dict(path=name, mode=mode, oid=oid, size=size))
    names={e['path'] for e in entries}
    # This is a minimum completeness contract, never an export allowlist:
    # every accepted blob in C:src is still exported unchanged.
    required = {'dossier.py', 'bootstrap.py', 'readme.md', 'readme_en.md', 'CHANGELOG.md', 'LICENSE',
                'tools/check-card.sh',
                'checks/run.sh', 'checks/check-env.sh', 'checks/lib/paths.sh'}
    required.update('rules/' + name + '.md' for name in (
        'claude-code', 'cursor', 'diagram', 'directory', 'naming', 'quotes',
        'roles', 'sources', 'verify', 'workflow'))
    required.update('dossier/' + name + '.py' for name in (
        '__init__', 'cli', 'install', 'paths', 'baseline', 'setup_probe', 'postman', 'release', 'runtime', 'factory',
        'ops/__init__', 'ops/close_cut', 'ops/cut_lock', 'ops/duty_probe', 'ops/section_stamp'))
    required.update('templates/' + name for name in (
        'CLAUDE.md', 'AGENTS.md', '.claude/settings.json', '.cursor/rules/switches.mdc',
        '.claude/agents/builder.md', '.claude/agents/contract-tester.md',
        '.claude/agents/review.md', '.claude/agents/spec-guard.md',
        '.codex/agents/builder.toml', '.codex/agents/contract-tester.toml',
        '.codex/agents/review.toml', '.codex/agents/spec-guard.toml',
        '.claude/skills/example-report/SKILL.md', '.claude/skills/one-slice/SKILL.md',
        '.claude/skills/write-cmd/SKILL.md'))
    required.update('rules/figures/' + name for name in (
        'dossier-frame.png', 'dossier-frame.render-stamp', 'dossier-icon.png',
        'dossier-icon.svg', 'dossier-icon-dark.png', 'dossier-icon-dark.svg', 'paradigm-shift.png'))
    missing=required-names
    if missing: raise ReleaseError('Incomplete product: '+', '.join(sorted(missing)))
    return dict(commit=commit, tree=tree, files=entries, count=len(entries), bytes=sum(e['size'] for e in entries))

def export(repo, snap, target):
    for entry in snap['files']:
        p=target.joinpath(*PurePosixPath(entry['path']).parts)
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(git(repo,'cat-file','blob',entry['oid']))
        p.chmod(0o755 if entry['mode']=='100755' else 0o644)

def checkout_metadata(repo, snap, product):
    """Give the new product its own exact tree and real HEAD, without remotes."""
    if (product / '.git').exists():
        raise ReleaseError('Product already has Git metadata')
    fmt = git(repo, 'rev-parse', '--show-object-format').decode().strip()
    git(product, 'init', '--quiet', '--template=', '--object-format=' + fmt)
    records = []
    for entry in snap['files']:
        oid = git(product, 'hash-object', '-w', '--stdin', data=git(repo, 'cat-file', 'blob', entry['oid'])).decode().strip()
        if oid != entry['oid']:
            raise ReleaseError('Exported object identity mismatch')
        records.append((entry['mode'] + ' ' + oid + '\t' + entry['path']).encode('utf-8') + b'\0')
    git(product, 'update-index', '-z', '--index-info', data=b''.join(records))
    tree = git(product, 'write-tree').decode().strip()
    if tree != snap['tree']:
        raise ReleaseError('Exported tree identity mismatch')
    message = f"Dossier local product checkout\n\nSource-commit: {snap['commit']}\nProduct-tree: {tree}\n"
    head = git(product, '-c', 'user.name=Dossier local build', '-c', 'user.email=build@invalid',
               'commit-tree', tree, data=message.encode()).decode().strip()
    git(product, 'update-ref', 'HEAD', head)

def validate(product):
    # Validate the directory users actually receive, with its own real source HEAD.
    def run(args):
        p=subprocess.run(args, cwd=product,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**git_environment(),'PYTHONDONTWRITEBYTECODE':'1'})
        if p.returncode:raise ReleaseError('Product validation failed: '+p.stdout.decode('utf-8','replace')[-4000:])
    run([sys.executable,'-B','-X','utf8',str(product/'dossier.py'),'--help'])
    with tempfile.TemporaryDirectory(prefix='dossier-host-') as tmp:
        host=Path(tmp)/'host';host.mkdir()
        run([sys.executable,'-B','-X','utf8',str(product/'dossier.py'),'init',str(host),'--non-interactive'])
        run([sys.executable,'-B','-X','utf8',str(product/'dossier.py'),'baseline',str(host)])

def remove_created(path):
    def writable_remove(func, name, exc):
        os.chmod(name, 0o700)
        func(name)
    shutil.rmtree(path, onerror=writable_remove)

def build(repo,snap,out):
    out=Path(out).absolute()
    if out.exists() or out.is_symlink():raise ReleaseError('Output already exists')
    if not out.parent.is_dir():raise ReleaseError('Output parent must exist')
    temp=Path(tempfile.mkdtemp(prefix='.dossier-build-',dir=out.parent))
    try:
        export(repo,snap,temp);checkout_metadata(repo,snap,temp);validate(temp)
        if out.exists():raise ReleaseError('Output appeared concurrently')
        temp.rename(out)
    finally:
        if temp.exists():remove_created(temp)

def formal_version(version):
    match = re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version)
    return tuple(map(int, match.groups())) if match else None

def branch_tip(repo, name):
    ref = 'refs/heads/' + name
    for line in git(repo,'worktree','list','--porcelain').decode().splitlines():
        if line == 'branch ' + ref: raise ReleaseError(name + ' is checked out in a worktree')
    symbolic=subprocess.run(['git','-C',str(repo),'symbolic-ref','-q',ref],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=git_environment())
    if symbolic.returncode==0:raise ReleaseError('Symbolic ' + name + ' reference is not supported')
    if symbolic.returncode not in (0,1):raise ReleaseError('Cannot inspect ' + name + ' reference')
    return git(repo,'rev-parse','--verify',ref,check=False).decode().strip()

def product_message(repo, commit, name):
    message=git(repo,'show','-s','--format=%B',commit).decode()
    if not message.startswith('Dossier product\n\nSource-commit: ') or '\nProduct-tree: ' not in message:
        raise ReleaseError('Unknown ' + name + ' history; refusing to take over')
    if git(repo,'rev-parse',commit+'^{tree}').decode().strip()!=message.split('Product-tree: ',1)[1].splitlines()[0]:
        raise ReleaseError('Unknown ' + name + ' tree')
    return message

def stable_version(repo, stable, dist):
    message = product_message(repo, stable, 'stable')
    if not dist or git(repo,'rev-list',stable,'--not',dist).strip():
        raise ReleaseError('stable is not in dist history')
    snapshot(repo, stable, product=True)
    versions = []
    for line in git(repo,'for-each-ref','--format=%(refname:strip=2) %(objecttype) %(*objectname)','refs/tags').decode().splitlines():
        fields = line.split()
        version = formal_version(fields[0]) if fields else None
        if version is not None and fields[1:] == ['tag', stable]:
            annotation = git(repo,'cat-file','-p','refs/tags/' + fields[0]).decode()
            if annotation.split('\n\n',1)[-1].strip() == message.strip():
                versions.append(version)
    if not versions: raise ReleaseError('stable has no formal Dossier product tag')
    return max(versions)

def publish(repo,snap,version):
    git(repo,'check-ref-format','refs/tags/'+version)
    if git(repo,'status','--porcelain','--untracked-files=no').strip():raise ReleaseError('Tracked worktree/index changes: commit source first')
    tagref='refs/tags/'+version
    existing=subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet',tagref],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=git_environment())
    if existing.returncode==0:raise ReleaseError('Tag already exists')
    if existing.returncode not in (0,1):raise ReleaseError('Cannot inspect existing tag')
    old=branch_tip(repo, 'dist')
    if old: product_message(repo, old, 'dist')
    stable=branch_tip(repo, 'stable')
    current=stable_version(repo, stable, old) if stable else None
    candidate=formal_version(version)
    tmp=Path(tempfile.mkdtemp(prefix='dossier-release-'))
    try:
        product=tmp/'product';product.mkdir();export(repo,snap,product);checkout_metadata(repo,snap,product);validate(product)
    finally:
        remove_created(tmp)
    ident=git(repo,'var','GIT_COMMITTER_IDENT').decode().strip()
    git(repo,'var','GIT_AUTHOR_IDENT')
    msg=f"Dossier product\n\nSource-commit: {snap['commit']}\nProduct-tree: {snap['tree']}\n"
    args=['commit-tree',snap['tree']]+(['-p',old] if old else [])
    new=git(repo,*args,data=msg.encode()).decode().strip()
    annotated=f"object {new}\ntype commit\ntag {version}\ntagger {ident}\n\n{msg}"
    tag=git(repo,'mktag',data=annotated.encode()).decode().strip()
    zero='0'*len(new)
    stable_update = candidate is not None and (current is None or candidate > current)
    stable_command = (f'update refs/heads/stable {new} {stable or zero}\n' if stable_update
                      else f'verify refs/heads/stable {stable or zero}\n')
    transaction=f'start\noption no-deref\nupdate refs/heads/dist {new} {old or zero}\ncreate {tagref} {tag}\n{stable_command}prepare\ncommit\n'
    git(repo,'update-ref','--stdin',data=transaction.encode())
    return dict(product_commit=new,tag=version,tag_oid=tag)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for command in ('preview','build','tag'):
        p=sub.add_parser(command);p.add_argument('--ref',default='HEAD')
        if command=='build':p.add_argument('--out',required=True)
        if command=='tag':
            p.add_argument('version');p.add_argument('--host-plan')
    args=parser.parse_args(argv)
    try:
        repo=repository();snap=snapshot(repo,args.ref)
        if args.command=='build':build(repo,snap,args.out)
        if args.command=='tag':
            from . import runtime
            from .paths import development_root
            host = development_root()
            value = None; plan_error = None
            if args.host_plan:
                value = json.loads(Path(args.host_plan).read_text(encoding='utf-8'))
            elif host is not None and (host / runtime.STATE).exists():
                try: value = runtime.plan(repo, args.ref, host)
                except (ReleaseError, OSError, ValueError) as exc: plan_error = str(exc)
            snap.update(publish(repo,snap,args.version))
            if value is not None:
                try: snap['host_update'] = runtime.apply(repo, args.version, value, value['host'])
                except (ReleaseError, OSError, ValueError, KeyError) as exc:
                    snap['host_update'] = dict(phase='failed', error=str(exc))
                    print(json.dumps(snap,ensure_ascii=False,indent=2));return 3
            elif host is not None or plan_error:
                snap['host_update'] = dict(phase='failed' if plan_error else 'unregistered', error=plan_error,
                                           message='Published; host runtime was not updated')
                print(json.dumps(snap,ensure_ascii=False,indent=2));return 3
        print(json.dumps(snap,ensure_ascii=False,indent=2));return 0
    except (ReleaseError,OSError,UnicodeError,ValueError) as exc:
        print('release: '+str(exc),file=sys.stderr);return 1
