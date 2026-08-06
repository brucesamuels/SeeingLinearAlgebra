#!/bin/zsh
set -euo pipefail
repo_root="${0:A:h:h}"
cd "$repo_root"
python -m py_compile engine/determinant_orientation.py scenes/determinant_orientation_presentation.py
python -m pytest -q tests/test_determinant_orientation.py tests/test_determinant_orientation_presentation.py
