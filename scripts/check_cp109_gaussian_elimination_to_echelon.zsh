#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_gaussian_elimination_to_echelon.py \
  tests/test_gaussian_elimination_to_echelon_presentation.py
