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
  -o CP151_r14_expanded_3d_rotation_preview \
  scenes/orthogonal_sets_presentation.py \
  OrthogonalSetsPresentation
