#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
python -m manim -pql scenes/matrix_composition_presentation.py MatrixCompositionPresentation
