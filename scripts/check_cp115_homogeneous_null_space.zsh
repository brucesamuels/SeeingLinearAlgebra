#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_homogeneous_null_space.py \
  tests/test_homogeneous_null_space_presentation.py
