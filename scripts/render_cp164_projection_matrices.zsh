#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m manim scenes/projection_matrices_presentation.py ProjectionMatricesPresentation "$@"
