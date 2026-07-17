#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_free_vector_equality.py \
  tests/test_free_vector_equality_lesson.py \
  tests/test_free_vector_equality_presentation.py

python -m pytest -q
