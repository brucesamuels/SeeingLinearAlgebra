#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP213 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP213 requires Manim Community v0.21.0."
  exit 1
}

python -m manim --disable_caching -ql \
  scenes/positive_definite_matrices_title_card.py \
  PositiveDefiniteMatricesTitleCard

python scripts/build_cp213_positive_definite_preview.py \
  --media-root media \
  --quality 480p15 \
  --output \
  media/videos/positive_definite_matrices_assembly/PositiveDefiniteMatrices_preview.mp4
