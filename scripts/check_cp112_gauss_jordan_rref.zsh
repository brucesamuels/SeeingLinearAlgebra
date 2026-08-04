#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_gauss_jordan_rref.py \
  tests/test_gauss_jordan_rref_presentation.py
