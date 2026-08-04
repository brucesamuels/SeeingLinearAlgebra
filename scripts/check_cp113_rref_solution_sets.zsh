#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_rref_solution_sets.py \
  tests/test_rref_solution_sets_presentation.py
