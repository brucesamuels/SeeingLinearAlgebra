#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim -pqh \
  scenes/rectangular_system_solvability_presentation.py \
  RectangularSystemSolvabilityPresentation
