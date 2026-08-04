#!/usr/bin/env zsh
set -euo pipefail

cd "${0:A:h}/.."
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

python -m manim --disable_caching -pql \
  scenes/elementary_row_operations_presentation.py \
  ElementaryRowOperationsPresentation
