#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_elementary_matrices.py \
  tests/test_elementary_matrices_presentation.py
