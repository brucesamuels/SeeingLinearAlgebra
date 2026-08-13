#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/orthogonal_sets.py \
  scenes/orthogonal_sets_presentation.py \
  tests/test_orthogonal_sets.py \
  tests/test_orthogonal_sets_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_orthogonal_sets.py \
  tests/test_orthogonal_sets_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import ThreeDAxes, ThreeDScene
from scenes.orthogonal_sets_presentation import OrthogonalSetsPresentation

assert issubclass(OrthogonalSetsPresentation, ThreeDScene)
assert OrthogonalSetsPresentation.SCENE_REVISION == "cp151_r14_expanded_3d_rotation"
print("CP151 r14 verified: expanded 3D camera rotation is installed.")
PY
