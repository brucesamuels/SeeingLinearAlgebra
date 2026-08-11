#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_determinant_chapter_synthesis.py \
  tests/test_determinant_chapter_synthesis_presentation.py \
  tests/test_cp147_scripts.py
