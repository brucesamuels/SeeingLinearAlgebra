#!/bin/zsh
set -euo pipefail

REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_two_vector_span.py \
  tests/test_two_vector_span_presentation.py

python -m pytest -q
