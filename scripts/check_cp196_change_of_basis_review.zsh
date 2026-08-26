#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/change_of_basis_review.py \
  scenes/change_of_basis_review_presentation.py
python -m pytest -q \
  tests/test_change_of_basis_review.py \
  tests/test_change_of_basis_review_presentation.py

print -- "Checkpoint 196 checks passed."

