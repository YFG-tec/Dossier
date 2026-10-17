"""Explicit source, host and ledger locations; no nearest-src discovery."""
from dataclasses import dataclass
from pathlib import Path
import subprocess

SOURCE_ROOT = Path(__file__).resolve().parents[1]

def development_root():
    """Recognize this tracked development layout, never a host's similarly named fixture."""
    root = SOURCE_ROOT.parent
    if SOURCE_ROOT.name != 'src' or not (root / 'tests/test_layout.py').is_file():
        return None
    try:
        top = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() != root:
            return None
        subprocess.run(['git', '-C', str(root), 'ls-files', '--error-unmatch', '--', 'src/dossier/paths.py', 'tests/test_layout.py', 'tests/mail/selftest.py'], capture_output=True, check=True)
        return root
    except (OSError, subprocess.CalledProcessError):
        return None

def default_host():
    if SOURCE_ROOT.parent.name == 'submodules':
        return SOURCE_ROOT.parent.parent
    return development_root() or SOURCE_ROOT

@dataclass(frozen=True)
class Locations:
    source: Path
    host: Path
    ledger: Path

def resolve(host_root=None, ledger_root=None):
    host = Path(host_root).resolve() if host_root is not None else default_host()
    ledger = Path(ledger_root).resolve() if ledger_root is not None else host / 'docs'
    return Locations(SOURCE_ROOT, host, ledger)

def execution_source(host_root=None):
    """Current host permissions come from verified A; product checks retain SOURCE_ROOT.

    An existing invalid registration is an error, never a fallback to B.
    """
    from .runtime import status, RuntimeError
    host = Path(host_root).resolve() if host_root is not None else default_host()
    result = status(host)
    if not result['ok']:
        raise RuntimeError('Invalid active runtime: ' + ', '.join(result['problems']))
    return Path(result['source']) if result['registered'] else SOURCE_ROOT
