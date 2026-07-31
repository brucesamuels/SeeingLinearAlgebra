#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."

python -m manim -pql \
  scenes/cross_product_computation_presentation.py \
  CrossProductComputationPresentation
