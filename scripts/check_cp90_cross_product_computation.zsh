#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pytest \
  tests/test_cross_product_computation.py \
  tests/test_cross_product_computation_presentation.py
