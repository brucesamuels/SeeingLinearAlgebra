#!/bin/zsh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q   tests/test_linear_combination_preservation.py   tests/test_linearity_preserves_linear_combinations_presentation.py
