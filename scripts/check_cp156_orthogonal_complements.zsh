#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/orthogonal_complements.py \
  scenes/orthogonal_complements_presentation.py \
  tests/test_orthogonal_complements.py \
  tests/test_orthogonal_complements_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_orthogonal_complements.py \
  tests/test_orthogonal_complements_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import ThreeDScene
from scenes.orthogonal_complements_presentation import OrthogonalComplementsPresentation

assert issubclass(OrthogonalComplementsPresentation, ThreeDScene)
assert OrthogonalComplementsPresentation.SCENE_REVISION == "cp156_r22_card4_caption_left_and_raise"
print("CP156 runtime verification passed.")
PY
