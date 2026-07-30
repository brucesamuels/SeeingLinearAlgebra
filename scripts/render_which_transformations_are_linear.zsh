#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="${0:A:h}"; REPO="${SCRIPT_DIR:h}"; cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
manim --disable_caching -pql scenes/which_transformations_are_linear_presentation.py WhichTransformationsAreLinearPresentation
