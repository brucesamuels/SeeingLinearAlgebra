#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_lesson_catalog.py \
  tests/test_seeing_linear_algebra_lesson_catalog.py

python -m pytest -q
