#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_matrix_vector_column_combination.py tests/test_matrix_vector_column_combination_presentation.py
