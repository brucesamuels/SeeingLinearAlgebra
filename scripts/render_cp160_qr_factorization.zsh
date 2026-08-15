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
  -o CP160_r4_right_title_clearance_preview.mp4 \
  scenes/qr_factorization_presentation.py \
  QRFactorizationPresentation
