#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}" \
python -m manim -pqh \
  scenes/multiple_right_hand_sides_presentation.py \
  MultipleRightHandSidesPresentation
