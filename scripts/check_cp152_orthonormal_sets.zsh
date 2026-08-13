#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/orthonormal_sets.py \
  scenes/orthonormal_sets_presentation.py \
  tests/test_orthonormal_sets.py \
  tests/test_orthonormal_sets_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_orthonormal_sets.py \
  tests/test_orthonormal_sets_presentation.py

PYTHONPATH=. python - <<'PY'
from manim import ThreeDScene
from scenes.orthonormal_sets_presentation import OrthonormalSetsPresentation

assert issubclass(OrthonormalSetsPresentation, ThreeDScene)
assert OrthonormalSetsPresentation.SCENE_REVISION == "cp152_r2_slower_transitions"
print("CP152 r2 verified: slower orthonormal-set pacing is installed.")
PY
