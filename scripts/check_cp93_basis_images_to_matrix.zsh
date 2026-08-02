#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_basis_images_to_matrix.py tests/test_basis_images_to_matrix_presentation.py
