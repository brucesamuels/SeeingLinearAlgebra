#!/bin/zsh
set -euo pipefail
repo_root="${0:A:h:h}"
cd "$repo_root"
python -m pytest -q \
  tests/test_determinant_properties.py \
  tests/test_determinant_properties_presentation.py
