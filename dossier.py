#!/usr/bin/env python3
"""Run this checkout, regardless of cwd or inherited PYTHONPATH."""
import importlib.util
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
package = root / 'dossier'
# Pin the package spec; a cwd dossier.py or inherited package cannot win.
for key in list(sys.modules):
    if key == 'dossier' or key.startswith('dossier.'):
        del sys.modules[key]
spec = importlib.util.spec_from_file_location('dossier', package / '__init__.py', submodule_search_locations=[str(package)])
module = importlib.util.module_from_spec(spec)
sys.modules['dossier'] = module
spec.loader.exec_module(module)
from dossier.cli import main
if __name__ == '__main__':
    raise SystemExit(main())
