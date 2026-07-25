#!/bin/zsh
set -euo pipefail

REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"

python -m pytest -q \
  tests/test_dimension_growth.py \
  tests/test_dimension_growth_presentation.py

python -m pytest -q
