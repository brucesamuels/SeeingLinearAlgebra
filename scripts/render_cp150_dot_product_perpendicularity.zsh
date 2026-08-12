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
  -o CP150_r6_verified_preview.mp4 \
  scenes/dot_product_perpendicularity_presentation.py \
  DotProductPerpendicularityPresentation
