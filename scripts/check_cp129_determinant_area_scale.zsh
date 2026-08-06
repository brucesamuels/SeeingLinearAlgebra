#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/determinant_area_scale.py \
  scenes/determinant_area_scale_presentation.py

python -m pytest -q \
  tests/test_determinant_area_scale.py \
  tests/test_determinant_area_scale_presentation.py

print "CP129 checks passed."
