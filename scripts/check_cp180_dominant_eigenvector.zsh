#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/dominant_eigenvector.py scenes/dominant_eigenvector_presentation.py
python -m pytest -q tests/test_dominant_eigenvector.py tests/test_dominant_eigenvector_presentation.py
