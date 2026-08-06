#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim -pqh scenes/rectangular_matrices_presentation.py RectangularMatricesPresentation
