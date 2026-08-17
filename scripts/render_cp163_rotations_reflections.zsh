#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m manim scenes/rotations_reflections_presentation.py RotationsReflectionsPresentation "$@"
