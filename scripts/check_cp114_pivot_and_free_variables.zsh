#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_pivot_and_free_variables.py \
  tests/test_pivot_and_free_variables_presentation.py
