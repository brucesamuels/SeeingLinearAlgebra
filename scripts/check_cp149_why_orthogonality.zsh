#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/why_orthogonality.py \
  scenes/why_orthogonality_presentation.py \
  tests/test_why_orthogonality.py \
  tests/test_why_orthogonality_presentation.py

python -m pytest -q \
  tests/test_why_orthogonality.py \
  tests/test_why_orthogonality_presentation.py

python - <<'PY'
from manim import Arrow, MathTex, NumberPlane, RightAngle
from scenes.why_orthogonality_presentation import WhyOrthogonalityPresentation

assert WhyOrthogonalityPresentation.CHAPTER_BANNER == "ORTHOGONALITY AND PROJECTION"
assert WhyOrthogonalityPresentation.LESSON_TITLE == "Why Orthogonality?"
print("CP149 Manim runtime imports verified.")
PY
