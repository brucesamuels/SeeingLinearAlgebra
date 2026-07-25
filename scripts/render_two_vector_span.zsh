#!/bin/zsh
set -euo pipefail

REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim -pql --disable_caching \
  scenes/two_vector_span_presentation.py \
  TwoVectorSpanPresentation
