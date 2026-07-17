#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python scripts/generate_lesson_inventory.py
python scripts/generate_lesson_inventory.py --check

python -m pytest -q \
  tests/test_lesson_inventory.py \
  tests/test_generate_lesson_inventory.py

python -m pytest -q
