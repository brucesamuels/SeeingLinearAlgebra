#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_rank_pivots_consistency.py \
  tests/test_rank_pivots_consistency_presentation.py
