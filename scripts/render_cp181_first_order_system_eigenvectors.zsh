#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
manim -pql scenes/first_order_system_eigenvectors_presentation.py FirstOrderSystemEigenvectorsPresentation
