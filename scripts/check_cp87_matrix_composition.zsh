#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
python -m pytest tests/test_matrix_composition.py tests/test_matrix_composition_presentation.py
