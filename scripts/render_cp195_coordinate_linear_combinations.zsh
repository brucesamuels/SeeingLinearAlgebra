#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
manim --disable_caching -pql \
  scenes/coordinate_linear_combinations_presentation.py \
  CoordinateLinearCombinationsPresentation

