#!/usr/bin/env zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
manim "$@" scenes/determinant_cofactor_expansion_presentation.py DeterminantCofactorExpansionPresentation
