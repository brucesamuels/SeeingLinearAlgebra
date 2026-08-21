#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/spectral_theorem.py scenes/spectral_theorem_presentation.py
python -m pytest -q tests/test_spectral_theorem.py tests/test_spectral_theorem_presentation.py
