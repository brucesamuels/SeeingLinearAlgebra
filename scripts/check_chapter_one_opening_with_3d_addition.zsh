#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q       tests/test_chapter_sequence.py       tests/test_chapter_one_opening_sequence.py       tests/test_chapter_one_opening_presentation.py       tests/test_chapter_one_opening_standard_position_integration.py       tests/test_chapter_one_opening_vector_addition_integration.py       tests/test_chapter_one_opening_three_vector_addition_integration.py

python -m pytest -q
