#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/least_squares_projection.py \
  scenes/least_squares_projection_presentation.py \
  tests/test_least_squares_projection.py \
  tests/test_least_squares_projection_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_least_squares_projection.py \
  tests/test_least_squares_projection_presentation.py

PYTHONPATH=. python - <<'PY'
from scenes.least_squares_projection_presentation import LeastSquaresProjectionPresentation

assert LeastSquaresProjectionPresentation.SCENE_REVISION == "cp161_r14_lower_penultimate_math_blocks"
print("CP161 runtime verification passed.")
PY
