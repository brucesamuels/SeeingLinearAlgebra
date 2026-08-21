#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/first_order_system_eigenvectors.py scenes/first_order_system_eigenvectors_presentation.py
python -m pytest -q tests/test_first_order_system_eigenvectors.py tests/test_first_order_system_eigenvectors_presentation.py
