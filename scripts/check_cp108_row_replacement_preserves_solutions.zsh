#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_row_replacement_preserves_solutions.py \
  tests/test_row_replacement_preserves_solutions_presentation.py
