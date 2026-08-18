#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/eigenvectors_eigenvalues.py \
  scenes/eigenvectors_eigenvalues_presentation.py \
  tests/test_eigenvectors_eigenvalues.py \
  tests/test_eigenvectors_eigenvalues_presentation.py

python -m pytest -q \
  tests/test_eigenvectors_eigenvalues.py \
  tests/test_eigenvectors_eigenvalues_presentation.py
