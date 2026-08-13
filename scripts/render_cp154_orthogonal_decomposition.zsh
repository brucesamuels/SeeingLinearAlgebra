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
  -o CP154_r2_labeled_geometry_preview \
  scenes/orthogonal_decomposition_presentation.py \
  OrthogonalDecompositionPresentation
