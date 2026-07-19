#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim       --disable_caching       -pql       scenes/vector_addition_commutativity_presentation.py       VectorAdditionCommutativityPresentation
