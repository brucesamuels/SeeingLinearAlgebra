#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pytest \
  tests/test_cross_product.py \
  tests/test_cross_product_presentation.py
