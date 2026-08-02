#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
manim --disable_caching -pql scenes/matrix_vector_column_combination_presentation.py MatrixVectorColumnCombinationPresentation
