#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_cp148_determinant_chapter_assembly.py \
  tests/test_cp148_scripts.py \
  tests/test_cp148_elimination_banner.py

python -m compileall -q \
  scenes/determinant_chapter_title_card.py \
  scripts/build_cp148_determinant_chapter.py
