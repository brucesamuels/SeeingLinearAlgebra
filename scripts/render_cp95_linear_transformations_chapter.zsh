#!/bin/zsh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python scripts/build_cp95_linear_transformations_chapter.py

OUTPUT="$REPO/media/videos/linear_transformations_chapter/LinearTransformationsChapter.mp4"

if [[ -f "$OUTPUT" ]]; then
  open "$OUTPUT"
else
  print -u2 "Expected chapter video was not created:"
  print -u2 "$OUTPUT"
  exit 1
fi
