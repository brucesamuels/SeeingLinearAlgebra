#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/eigenvalues_chapter_review.py scenes/eigenvalues_chapter_review_presentation.py
python -m pytest -q tests/test_eigenvalues_chapter_review.py tests/test_eigenvalues_chapter_review_presentation.py
