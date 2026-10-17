"""Install a fixed product using its own installer (Python standard library and Git)."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen


def canonical(repository):
    value = str(repository).rstrip('/')
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([\w.-]+)/([\w.-]+?)(?:\.git)?', value)
    if match:
        return 'https://github.com/' + '/'.join(match.groups()) + '.git'
    if '://' not in value and not value.startswith('git@'):
        return str(Path(value).resolve())
    return value


def select(repository, version=None):
    repository = canonical(repository)
    if version:
        if version.startswith('-'): raise ValueError('Invalid version')
        return repository, version
    match = re.fullmatch(r'https://github\.com/([\w.-]+)/([\w.-]+)\.git', repository)
    if not match: raise ValueError('Non-GitHub repositories require --version')
    request = Request('https://api.github.com/repos/' + '/'.join(match.groups()) + '/releases/latest',
                      headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Dossier-bootstrap'})
    with urlopen(request, timeout=30) as response:
        release = json.load(response)
    tag = release.get('tag_name')
    if release.get('draft') is not False or release.get('prerelease') is not False or not isinstance(tag, str) or not tag.strip() or tag.startswith('-'):
        raise ValueError('Latest response is not a formal release')
    return repository, tag


def git(repo, *args):
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    proc = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, env=environment)
    if proc.returncode: raise ValueError(proc.stderr.decode('utf-8', 'replace'))
    return proc.stdout.decode().strip()


def obtain(repository, version, directory):
    directory = Path(directory)
    directory.mkdir()
    git(directory, 'init', '--quiet', '--template=')
    git(directory, 'fetch', '--no-tags', repository, version)
    commit = git(directory, 'rev-parse', 'FETCH_HEAD^{commit}')
    git(directory, 'checkout', '--detach', commit)
    # Inspect Git objects before executing any code from the selected product.
    entries = git(directory, 'ls-tree', '-rz', commit).split('\0')
    names = set()
    forbidden = {'.git', '.mail', '.dossier', '.venv', '.tmp', '__pycache__', 'node_modules', 'docs', 'examples'}
    for entry in entries:
        if not entry: continue
        meta, name = entry.split('\t', 1)
        mode, kind, oid = meta.split()
        parts = name.split('/')
        if mode not in ('100644', '100755') or kind != 'blob' or any(x in forbidden or x in ('', '.', '..') or ':' in x or '\\' in x or x.lower().startswith('.env') or x.lower().endswith(('.pyc', '.pem', '.key')) or x.lower() in ('settings.local.json', 'credentials.json', 'todo.md', 'session.md') for x in parts):
            raise ValueError('Unsafe product entry: ' + name)
        if len(parts) >= 2 and [p.casefold() for p in parts[:2]] == ['tools', 'figures']:
            raise ValueError('Development figure tools in product: ' + name)
        if name.casefold() in names: raise ValueError('Case-colliding product entries')
        names.add(name.casefold())
    required = {'bootstrap.py', 'dossier.py', 'readme.md', 'readme_en.md', 'changelog.md', 'license', 'checks/check-env.sh', 'checks/lib/paths.sh', 'checks/run.sh'}
    required.update('dossier/' + x + '.py' for x in ('__init__', 'cli', 'install', 'paths', 'baseline', 'setup_probe', 'postman', 'release', 'runtime', 'factory', 'ops/__init__', 'ops/close_cut', 'ops/cut_lock', 'ops/duty_probe', 'ops/section_stamp'))
    required.update('rules/' + x + '.md' for x in ('claude-code', 'cursor', 'diagram', 'directory', 'naming', 'quotes', 'roles', 'sources', 'verify', 'workflow'))
    required.update('templates/' + x for x in ('claude.md', 'agents.md', '.claude/settings.json', '.cursor/rules/switches.mdc'))
    required.update('templates/' + folder + '/' + name + suffix for folder, suffix in (('.claude/agents', '.md'), ('.codex/agents', '.toml')) for name in ('builder', 'contract-tester', 'review', 'spec-guard'))
    required.update('templates/.claude/skills/' + name + '/skill.md' for name in ('example-report', 'one-slice', 'write-cmd'))
    required.add('tools/check-card.sh')
    required.update('rules/figures/' + name for name in ('dossier-frame.png', 'dossier-frame.render-stamp', 'dossier-icon.png', 'dossier-icon.svg', 'dossier-icon-dark.png', 'dossier-icon-dark.svg', 'paradigm-shift.png'))
    if not required.issubset(names) or 'src/dossier.py' in names:
        raise ValueError('Selected version is not a complete product root')
    return commit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--host-root', required=True)
    parser.add_argument('--version', help='Explicit formal tag or commit; skips latest lookup')
    args = parser.parse_args(argv)
    try:
        # Existing installations never query latest or rerun an installer.
        installed = Path(args.host_root).resolve() / 'submodules/dossier/dossier.py'
        if installed.is_file():
            return subprocess.call([sys.executable, '-B', str(installed), 'factory', 'install', '--host-root', args.host_root,
                                    '--repository', args.repository] + (['--version', args.version] if args.version else []))
        repository, version = select(args.repository, args.version)
        with tempfile.TemporaryDirectory(prefix='dossier-bootstrap-') as tmp:
            product = Path(tmp) / 'product'
            commit = obtain(repository, version, product)
            return subprocess.call([sys.executable, '-B', str(product / 'dossier.py'), 'factory', 'install',
                                    '--repository', repository, '--version', commit, '--host-root', args.host_root])
    except (ValueError, OSError) as exc:
        print('bootstrap: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
