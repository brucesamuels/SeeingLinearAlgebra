#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused native 3D linear-combination tests..."
python -m pytest -q tests/test_linear_combination_native_3d_smoke.py

print "Running complete test suite..."
python -m pytest -q
