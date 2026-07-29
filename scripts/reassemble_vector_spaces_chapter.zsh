#!/bin/zsh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"

DURATION_FACTOR="${1:-1.25}"
BUILD_DIR="$REPO_DIR/media/chapter_build/vector_spaces"
CONCAT_FILE="$BUILD_DIR/concat.txt"
OUTPUT_DIR="$REPO_DIR/media/videos/vector_spaces_chapter/480p15"
OUTPUT_FILE="$OUTPUT_DIR/VectorSpacesAndSubspacesChapter.mp4"

if [[ ! -f "$CONCAT_FILE" ]]; then
  print -u2 -- "Chapter segment list not found: $CONCAT_FILE"
  print -u2 -- "Run ./scripts/render_vector_spaces_chapter.zsh once to render the segments."
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
print -- "Reassembling existing chapter segments at ${DURATION_FACTOR}x duration..."
python scripts/assemble_vector_spaces_chapter.py \
  "$CONCAT_FILE" \
  "$OUTPUT_FILE" \
  --duration-factor "$DURATION_FACTOR"

print -- ""
print -- "Chapter reassembly complete:"
print -- "$OUTPUT_FILE"
