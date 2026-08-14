#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

args=("$@")
if (( ${#args[@]} == 0 )); then
  args=(-pql)
fi

python -m manim --disable_caching \
  $args \
  -o CP157_r6_card2_marker_natural_quadrant_preview.mp4 \
  scenes/gram_schmidt_two_vectors_presentation.py \
  GramSchmidtTwoVectorsPresentation
