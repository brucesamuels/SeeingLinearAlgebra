#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_special_vectors_lesson.py \
  tests/test_special_vectors_presentation.py

python -m pytest -q
