#!/usr/bin/env zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q \
  tests/test_determinant_cramers_rule.py \
  tests/test_determinant_cramers_rule_presentation.py \
  tests/test_cp141_scripts.py
python -m compileall -q engine scenes tests
