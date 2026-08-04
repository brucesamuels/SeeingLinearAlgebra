#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_null_space_basis.py \
  tests/test_null_space_basis_presentation.py
