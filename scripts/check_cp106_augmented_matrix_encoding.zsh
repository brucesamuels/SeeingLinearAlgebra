#!/usr/bin/env zsh
set -euo pipefail

cd "${0:A:h}/.."
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "== CP106 focused tests =="
python -m pytest -q \
  tests/test_augmented_matrix_encoding.py \
  tests/test_augmented_matrix_encoding_presentation.py

echo
echo "== Complete repository test suite =="
python -m pytest -q
