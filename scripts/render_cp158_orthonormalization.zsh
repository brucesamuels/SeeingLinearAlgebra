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
  -o CP158_r3_grid_on_all_graphic_cards_preview.mp4 \
  scenes/orthonormalization_presentation.py \
  OrthonormalizationPresentation
