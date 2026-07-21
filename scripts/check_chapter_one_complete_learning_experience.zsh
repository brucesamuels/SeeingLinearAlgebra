#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO=${SCRIPT_DIR:h}

cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_chapter_learning_experience.py \
  tests/test_chapter_orchestration.py \
  tests/test_chapter_one_opening_sequence.py \
  tests/test_chapter_one_learning_experience_integration.py \
  tests/test_special_vectors_lesson.py \
  tests/test_special_vectors_presentation.py \
  tests/test_coefficient_choreography.py \
  tests/test_infinite_possibilities_presentation.py

python -m pytest -q
