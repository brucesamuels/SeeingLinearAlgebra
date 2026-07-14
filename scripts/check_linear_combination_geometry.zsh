#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
python -m pytest -q tests/test_linear_combination_geometry.py
