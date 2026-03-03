#!/usr/bin/env bash

# Run the easy-screenshot tool
# Pass any arguments through to the module, e.g.:
#   ./run.sh --select
#   ./run.sh --application Terminal
#   ./run.sh --help

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$REPO_ROOT/source_me.sh"

# Make the local package importable when invoked outside the repo root.
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

if [[ -x "/opt/homebrew/opt/python@3.12/bin/python3.12" ]]; then
  PYTHON_BIN="/opt/homebrew/opt/python@3.12/bin/python3.12"
elif command -v python3.12 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3.12)"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
else
  echo "Error: could not find a Python interpreter." >&2
  exit 1
fi

exec "$PYTHON_BIN" -m screenshot.screencapture "$@"
