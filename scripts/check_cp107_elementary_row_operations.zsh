#!/usr/bin/env zsh
set -euo pipefail

cd "${0:A:h}/.."
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "== CP107 focused tests =="
python -m pytest -q \
  tests/test_elementary_row_operations.py \
  tests/test_elementary_row_operations_presentation.py

echo
echo "== Complete repository test suite =="
python -m pytest -q
