#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python scripts/generate_lesson_inventory.py
python scripts/generate_lesson_inventory_json.py

python scripts/generate_lesson_inventory.py --check
python scripts/generate_lesson_inventory_json.py --check
python scripts/verify_lesson_documentation.py

python -m pytest -q \
  tests/test_lesson_documentation_verification.py \
  tests/test_verify_lesson_documentation_script.py

python -m pytest -q
