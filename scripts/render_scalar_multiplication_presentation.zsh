#!/bin/zsh
set -euo pipefail

REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"

python -m manim -pql \
  scenes/scalar_multiplication_presentation.py \
  ScalarMultiplicationPresentation
