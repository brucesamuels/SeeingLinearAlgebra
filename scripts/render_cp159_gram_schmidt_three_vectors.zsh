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
  -o CP159_r6_card5_pairwise_views_preview.mp4 \
  scenes/gram_schmidt_three_vectors_presentation.py \
  GramSchmidtThreeVectorsPresentation
