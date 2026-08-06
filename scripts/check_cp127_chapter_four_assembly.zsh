#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q tests/test_cp127_chapter_four_assembly.py
python -m py_compile \
  scenes/chapter_four_title_card.py \
  scripts/build_cp127_chapter_four.py
