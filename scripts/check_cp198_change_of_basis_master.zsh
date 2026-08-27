#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile scripts/build_cp198_change_of_basis_master.py
zsh -n scripts/render_cp198_change_of_basis_master.zsh
python -m pytest -q \
  tests/test_change_of_basis_master_assembly.py \
  tests/test_change_of_basis_master_render_script.py

print -- "Checkpoint 198 high-definition master checks passed."

