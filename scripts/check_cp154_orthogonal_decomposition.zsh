#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/orthogonal_decomposition.py \
  scenes/orthogonal_decomposition_presentation.py \
  tests/test_orthogonal_decomposition.py \
  tests/test_orthogonal_decomposition_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_orthogonal_decomposition.py \
  tests/test_orthogonal_decomposition_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import Scene
from scenes.orthogonal_decomposition_presentation import OrthogonalDecompositionPresentation

assert issubclass(OrthogonalDecompositionPresentation, Scene)
assert OrthogonalDecompositionPresentation.SCENE_REVISION == "cp154_r2_labeled_geometry"
print("CP154 r2 verified: labeled orthogonal-decomposition geometry is installed.")
PY
