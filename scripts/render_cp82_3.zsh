#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO="${SCRIPT_DIR:h}"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

manim --disable_caching -pql   scenes/what_does_a_linear_transformation_do_presentation.py   WhatDoesALinearTransformationDoPresentation
