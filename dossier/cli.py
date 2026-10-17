"""Thin command routing; module argument semantics stay with each tool."""
import importlib
import sys
from pathlib import Path
from .paths import SOURCE_ROOT, resolve

COMMANDS = {'init': 'install', 'baseline': 'baseline', 'postman': 'postman',
            'setup-probe': 'setup_probe', 'close-cut': 'ops.close_cut',
            'cut-lock': 'ops.cut_lock', 'duty-probe': 'ops.duty_probe',
            'section-stamp': 'ops.section_stamp', 'release': 'release', 'runtime': 'runtime', 'factory': 'factory'}

def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ('-h', '--help'):
        print('Dossier commands: ' + ', '.join(COMMANDS))
        print('Source: ' + str(SOURCE_ROOT))
        print('Use <command> --help; --host-root HOST selects the operated desk.')
        return 0
    command = args.pop(0)
    if command not in COMMANDS:
        print('Unknown command: ' + command, file=sys.stderr)
        return 2
    if command in ('release', 'runtime', 'factory'):
        return importlib.import_module('dossier.' + command).main(args)
    host = None
    if '--host-root' in args:
        i = args.index('--host-root')
        if i + 1 == len(args):
            print('--host-root requires HOST', file=sys.stderr); return 2
        host = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    module = importlib.import_module('dossier.' + COMMANDS[command])
    target_command = command in ('init', 'baseline', 'setup-probe')
    if command in ('close-cut', 'cut-lock', 'duty-probe'):
        target = host if host is not None else resolve().host
        module.REPO = target
        if hasattr(module, 'LOCKS'): module.LOCKS = target / '.tmp' / 'locks'
        if hasattr(module, 'WAKE'): module.WAKE = target / '.tmp' / 'queue-runner' / 'wake.md'
    elif host is not None and command == 'postman':
        # Existing mailbox discovery is cwd-based; make this explicit, not source-based.
        import os
        old = Path.cwd()
        try:
            os.chdir(host)
            return module.main(args)
        finally:
            os.chdir(old)
    elif host is not None and not target_command:
        print('--host-root is not applicable to source stamps', file=sys.stderr); return 2
    before = sys.argv
    try:
        sys.argv = [str(SOURCE_ROOT / 'dossier.py') + ' ' + command] + args
        return (module.main(host_root=host) if target_command else module.main()) or 0
    finally:
        sys.argv = before
