#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  scenes/change_of_basis_title_card.py \
  scripts/build_cp197_change_of_basis_preview.py
python -m pytest -q \
  tests/test_change_of_basis_title_card.py \
  tests/test_change_of_basis_preview_assembly.py

print -- "Checkpoint 197 preview-assembly checks passed."

