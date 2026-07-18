#!/bin/zsh
set -euo pipefail

REPO=${0:A:h:h}
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim -pql --disable_caching \
  scenes/placing_vector_at_origin_presentation.py \
  PlacingVectorAtOriginPresentation
