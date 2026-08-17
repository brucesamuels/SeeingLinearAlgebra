#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m py_compile \
  engine/rotations_reflections.py \
  scenes/rotations_reflections_presentation.py \
  tests/test_rotations_reflections.py \
  tests/test_rotations_reflections_presentation.py

PYTHONPATH=. pytest -q \
  tests/test_rotations_reflections.py \
  tests/test_rotations_reflections_presentation.py
