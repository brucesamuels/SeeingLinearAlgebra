#!/usr/bin/env zsh
set -euo pipefail

cd "${0:A:h}/.."
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

echo "== CP105 focused tests =="
python -m pytest -q \
  tests/test_linear_system_meaning.py \
  tests/test_linear_system_meaning_presentation.py

echo
echo "== Complete repository test suite =="
python -m pytest -q
