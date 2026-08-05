#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_multiple_right_hand_sides.py \
  tests/test_multiple_right_hand_sides_presentation.py
