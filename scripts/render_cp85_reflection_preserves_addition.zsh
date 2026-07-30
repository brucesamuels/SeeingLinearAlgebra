#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
manim --disable_caching -pql   scenes/reflection_preserves_addition_presentation.py   ReflectionPreservesAdditionPresentation
