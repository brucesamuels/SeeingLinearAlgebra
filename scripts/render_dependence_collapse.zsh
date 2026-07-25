#!/bin/zsh
set -euo pipefail
REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
manim -pql --disable_caching scenes/dependence_collapse_presentation.py DependenceCollapsePresentation
