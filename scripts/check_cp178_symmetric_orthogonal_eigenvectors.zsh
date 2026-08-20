#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/symmetric_orthogonal_eigenvectors.py scenes/symmetric_orthogonal_eigenvectors_presentation.py
python -m pytest -q tests/test_symmetric_orthogonal_eigenvectors.py tests/test_symmetric_orthogonal_eigenvectors_presentation.py
