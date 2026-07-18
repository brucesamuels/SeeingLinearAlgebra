#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q       tests/test_three_vector_addition.py       tests/test_three_vector_addition_lesson.py       tests/test_three_vector_addition_presentation.py

python -m pytest -q
