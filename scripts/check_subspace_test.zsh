#!/bin/zsh
set -euo pipefail
REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_subspace_test.py tests/test_subspace_test_presentation.py
