#!/bin/zsh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"
pytest \
  tests/test_vector_spaces_chapter.py \
  tests/test_vector_spaces_chapter_cards.py \
  tests/test_vector_spaces_chapter_render_script.py \
  tests/test_vector_spaces_chapter_pacing.py
