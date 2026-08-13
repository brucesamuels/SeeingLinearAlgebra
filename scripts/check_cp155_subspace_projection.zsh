#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/subspace_projection.py \
  scenes/subspace_projection_presentation.py \
  tests/test_subspace_projection.py \
  tests/test_subspace_projection_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_subspace_projection.py \
  tests/test_subspace_projection_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import ThreeDScene
from scenes.subspace_projection_presentation import SubspaceProjectionPresentation

assert issubclass(SubspaceProjectionPresentation, ThreeDScene)
assert SubspaceProjectionPresentation.SCENE_REVISION == "cp155_r4_card3_spacing_and_smoother_labels"
print("CP155 r2 verified: general-basis projection lesson is installed.")
PY
