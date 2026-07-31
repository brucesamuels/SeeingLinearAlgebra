#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pytest tests/test_inner_product.py tests/test_inner_product_dot_product_presentation.py
