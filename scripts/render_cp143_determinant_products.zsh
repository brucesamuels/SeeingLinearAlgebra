#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

quality="${1:--pql}"
python -m manim --disable_caching "$quality" \
  scenes/determinant_product_rule_presentation.py \
  DeterminantProductRulePresentation
