#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
PYTHONPATH="$REPO_ROOT" python -m pytest -q tests/test_coefficient_sweep_path.py
