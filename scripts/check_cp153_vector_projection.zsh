#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/vector_projection.py \
  scenes/vector_projection_presentation.py \
  tests/test_vector_projection.py \
  tests/test_vector_projection_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_vector_projection.py \
  tests/test_vector_projection_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import Scene
from scenes.vector_projection_presentation import VectorProjectionPresentation

assert issubclass(VectorProjectionPresentation, Scene)
assert VectorProjectionPresentation.SCENE_REVISION == "cp153_r2_left_import_hotfix"
print("CP153 r2 verified: geometric vector-projection lesson is installed.")
PY
