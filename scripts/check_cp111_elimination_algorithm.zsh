#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_elimination_algorithm.py \
  tests/test_elimination_algorithm_presentation.py
