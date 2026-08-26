#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
manim --disable_caching -pql \
  scenes/change_of_basis_review_presentation.py \
  ChangeOfBasisReviewPresentation

