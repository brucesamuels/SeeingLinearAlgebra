#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}" \
python -m manim -pqh \
  scenes/gauss_jordan_inverse_presentation.py \
  GaussJordanInversePresentation
