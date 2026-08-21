#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/fibonacci_difference_equation.py scenes/fibonacci_difference_equation_presentation.py
python -m pytest -q tests/test_fibonacci_difference_equation.py tests/test_fibonacci_difference_equation_presentation.py
