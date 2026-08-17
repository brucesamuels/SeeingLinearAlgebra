#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m py_compile \
  engine/chapter_six_finale.py \
  scenes/chapter_six_finale_presentation.py \
  tests/test_chapter_six_finale.py \
  tests/test_chapter_six_finale_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_chapter_six_finale.py \
  tests/test_chapter_six_finale_presentation.py
