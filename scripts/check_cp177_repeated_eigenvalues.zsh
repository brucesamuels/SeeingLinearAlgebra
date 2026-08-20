#!/bin/zsh
set -euo pipefail
repo_root="${0:A:h:h}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/repeated_eigenvalues.py scenes/repeated_eigenvalues_presentation.py
python -m pytest -q tests/test_repeated_eigenvalues.py tests/test_repeated_eigenvalues_presentation.py
