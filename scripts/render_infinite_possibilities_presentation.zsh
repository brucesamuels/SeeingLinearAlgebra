#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -pql \
  scenes/infinite_possibilities_presentation.py \
  InfinitePossibilitiesPresentation
