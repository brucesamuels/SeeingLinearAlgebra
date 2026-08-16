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
  -o CP161_r14_lower_penultimate_math_blocks_preview.mp4 \
  scenes/least_squares_projection_presentation.py \
  LeastSquaresProjectionPresentation
