#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim -pqh scenes/pivoting_pa_lu_presentation.py PivotingPALUPresentation
