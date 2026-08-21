#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
manim -pql scenes/characteristic_equation_presentation.py CharacteristicEquationPresentation
manim -pql scenes/symmetric_orthogonal_eigenvectors_presentation.py SymmetricOrthogonalEigenvectorsPresentation
