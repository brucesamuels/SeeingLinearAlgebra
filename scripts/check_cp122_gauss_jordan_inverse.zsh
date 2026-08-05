#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_gauss_jordan_inverse.py \
  tests/test_gauss_jordan_inverse_presentation.py
