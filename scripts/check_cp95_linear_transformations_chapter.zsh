#!/bin/zsh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q tests/test_cp95_linear_transformations_chapter.py
python -m py_compile \
  scenes/linear_transformations_chapter_cards.py \
  scripts/build_cp95_linear_transformations_chapter.py
