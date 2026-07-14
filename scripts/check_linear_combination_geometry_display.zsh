#!/bin/zsh
set -euo pipefail

REPO_ROOT=${0:A:h:h}
cd "$REPO_ROOT"
python -m pytest -q tests/test_linear_combination_geometry_display.py
