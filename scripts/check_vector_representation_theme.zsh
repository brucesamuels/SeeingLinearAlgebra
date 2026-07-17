#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_vector_representation_presentation.py \
  tests/test_vector_representation_magnitude_label_refinement.py \
  tests/test_vector_representation_theme_integration.py

python -m pytest -q
