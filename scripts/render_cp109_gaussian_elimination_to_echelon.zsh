#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m manim -pqh \
  scenes/gaussian_elimination_to_echelon_presentation.py \
  GaussianEliminationToEchelonPresentation
