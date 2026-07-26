#!/bin/zsh
set -euo pipefail
REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_column_space.py tests/test_column_space_presentation.py
