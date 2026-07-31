#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
python -m manim -pql scenes/inner_product_dot_product_presentation.py InnerProductDotProductPresentation
