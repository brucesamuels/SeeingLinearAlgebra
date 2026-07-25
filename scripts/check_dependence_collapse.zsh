#!/bin/zsh
set -euo pipefail
REPO="/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_dependence_collapse.py tests/test_dependence_collapse_presentation.py
python -m pytest -q
