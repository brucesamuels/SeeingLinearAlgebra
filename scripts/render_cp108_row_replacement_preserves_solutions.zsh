#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m manim -pqh \
  scenes/row_replacement_preserves_solutions_presentation.py \
  RowReplacementPreservesSolutionsPresentation
