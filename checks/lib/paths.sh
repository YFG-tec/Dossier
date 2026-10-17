#!/usr/bin/env bash
DOSSIER_SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
DOSSIER_HOST_ROOT="${DOSSIER_HOST_ROOT:-$DOSSIER_SOURCE_ROOT}"
if [[ "${1:-}" == --host-root ]]; then
  [[ $# -ge 2 ]] || { echo '--host-root requires a path' >&2; exit 2; }
  DOSSIER_HOST_ROOT="$(cd "$2" && pwd -P)" || exit 2
  shift 2
fi
[[ $# -eq 0 ]] || { echo 'unexpected check arguments' >&2; exit 2; }
ROOT="$DOSSIER_HOST_ROOT"
cd "$DOSSIER_SOURCE_ROOT" || exit 2
