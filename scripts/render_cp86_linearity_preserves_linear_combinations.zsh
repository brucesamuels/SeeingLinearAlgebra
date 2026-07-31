#!/bin/zsh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim --disable_caching -pql   scenes/linearity_preserves_linear_combinations_presentation.py   LinearityPreservesLinearCombinationsPresentation
