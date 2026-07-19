#!/bin/zsh
set -euo pipefail

REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"

python -m pytest -q \
  tests/test_scalar_multiplication_lesson.py \
  tests/test_scalar_multiplication_presentation.py \
  tests/test_scalar_multiplication_audit.py \
  tests/test_linear_combination.py \
  tests/test_coefficient_sweep_path.py

python -m pytest -q
