#!/usr/bin/env zsh
set -euo pipefail
quality=${1:- -pqh}
python -m manim --disable_caching $quality scenes/determinant_big_formula_presentation.py DeterminantBigFormulaPresentation
