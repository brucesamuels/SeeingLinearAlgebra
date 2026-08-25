#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/transformation_between_bases.py scenes/transformation_between_bases_presentation.py
python -m pytest -q tests/test_transformation_between_bases.py tests/test_transformation_between_bases_presentation.py
