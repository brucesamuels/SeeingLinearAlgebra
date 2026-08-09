#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_determinant_product_rule.py \
  tests/test_determinant_product_rule_presentation.py \
  tests/test_cp143_scripts.py
