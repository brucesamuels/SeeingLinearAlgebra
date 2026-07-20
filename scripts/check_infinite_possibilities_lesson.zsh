#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_coefficient_choreography.py \
  tests/test_infinite_possibilities_presentation.py

python -m pytest -q
