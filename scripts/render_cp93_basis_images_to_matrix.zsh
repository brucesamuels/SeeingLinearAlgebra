#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
manim --disable_caching -pql scenes/basis_images_to_matrix_presentation.py BasisImagesToMatrixPresentation
