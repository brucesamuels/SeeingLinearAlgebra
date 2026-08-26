#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

manim --disable_caching -ql \
  scenes/change_of_basis_title_card.py \
  ChangeOfBasisTitleCard

python scripts/build_cp197_change_of_basis_preview.py \
  --media-root media \
  --quality 480p15 \
  --output media/change_of_basis_preview.mp4

preview="$repo_root/media/change_of_basis_preview.mp4"
if [[ "$(uname -s)" == "Darwin" ]]; then
  open "$preview"
else
  print -- "Preview ready: $preview"
fi

