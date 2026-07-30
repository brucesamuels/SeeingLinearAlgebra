#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO="${SCRIPT_DIR:h}"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_planar_affine_transformation.py \
  tests/test_what_does_a_linear_transformation_do_presentation.py

python -m pytest -q
