#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -pql \
  scenes/special_vectors_presentation.py \
  SpecialVectorsPresentation
