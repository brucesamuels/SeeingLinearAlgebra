#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/chapter_one_lesson_manifest.py \
  scenes/chapter_one_title_card.py \
  scripts/build_cp91_chapter_one.py \
  tests/test_cp91_chapter_one_assembly.py

python -m pytest -q tests/test_cp91_chapter_one_assembly.py
