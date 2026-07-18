#!/bin/zsh
set -euo pipefail

REPO=${0:A:h:h}
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_vector_to_origin_translation.py \
  tests/test_manim_vector_to_origin_display.py \
  tests/test_placing_vector_at_origin_presentation.py

python -m pytest -q
