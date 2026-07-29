#!/bin/zsh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"

QUALITY="${1:--pql}"
DURATION_FACTOR="${2:-1.25}"
BUILD_DIR="$REPO_DIR/media/chapter_build/vector_spaces"
MEDIA_DIR="$BUILD_DIR/media"
CONCAT_FILE="$BUILD_DIR/concat.txt"

if [[ ! -f "$CONCAT_FILE" ]]; then
  print -u2 -- "Chapter segment list not found: $CONCAT_FILE"
  print -u2 -- "Run ./scripts/render_vector_spaces_chapter.zsh once before using this focused rerender."
  exit 1
fi

mkdir -p "$MEDIA_DIR"

print -- "Rerendering only the chapter-opening card..."
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" \
  scenes/vector_spaces_chapter_cards.py \
  VectorSpacesChapterOpening

print -- "Reassembling the existing chapter at ${DURATION_FACTOR}x duration..."
./scripts/reassemble_vector_spaces_chapter.zsh "$DURATION_FACTOR"
