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
  -o CP156_r22_card4_caption_left_and_raise_preview.mp4 \
  scenes/orthogonal_complements_presentation.py \
  OrthogonalComplementsPresentation
