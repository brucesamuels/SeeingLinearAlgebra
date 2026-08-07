#!/usr/bin/env zsh
set -euo pipefail
python -m pytest -q tests/test_determinant_big_formula_derivation.py tests/test_determinant_big_formula_derivation_presentation.py
python -m compileall -q engine scenes tests
