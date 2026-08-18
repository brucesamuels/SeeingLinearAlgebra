#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/characteristic_equation.py \
  scenes/characteristic_equation_presentation.py \
  tests/test_characteristic_equation.py \
  tests/test_characteristic_equation_presentation.py

python -m pytest -q \
  tests/test_characteristic_equation.py \
  tests/test_characteristic_equation_presentation.py
