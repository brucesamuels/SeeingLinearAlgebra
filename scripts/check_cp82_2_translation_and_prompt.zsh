#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO="${SCRIPT_DIR:h}"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q tests/test_cp82_2_translation_and_prompt_refinement.py
python -m pytest -q
