#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}" \
python -m manim -pqh \
  scenes/homogeneous_null_space_presentation.py \
  HomogeneousNullSpacePresentation
