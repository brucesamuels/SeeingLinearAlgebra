#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile \
  scenes/chapter_seven_title_card.py \
  scripts/build_cp184_chapter_seven.py
python -m pytest -q tests/test_cp184_chapter_seven_assembly.py
