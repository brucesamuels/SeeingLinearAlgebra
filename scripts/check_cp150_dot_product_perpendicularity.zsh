#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/dot_product_perpendicularity.py \
  scenes/dot_product_perpendicularity_presentation.py \
  tests/test_dot_product_perpendicularity.py \
  tests/test_dot_product_perpendicularity_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_dot_product_perpendicularity.py \
  tests/test_dot_product_perpendicularity_presentation.py

grep -q 'CP150_REVISION = "r6_verified_split_layout_test_fix"' \
  scenes/dot_product_perpendicularity_presentation.py
print -- "CP150 r6 source verification passed."

PYTHONPATH=. python - <<'PY'
from manim import Arc, Arrow, MathTex, NumberPlane, RightAngle, SurroundingRectangle
from scenes.dot_product_perpendicularity_presentation import DotProductPerpendicularityPresentation

assert DotProductPerpendicularityPresentation.CHAPTER_BANNER == "ORTHOGONALITY AND PROJECTION"
assert DotProductPerpendicularityPresentation.LESSON_TITLE == "Dot Product and Perpendicularity"
assert DotProductPerpendicularityPresentation.CP150_REVISION == "r6_verified_split_layout_test_fix"
print("CP150 Manim runtime imports verified.")
PY
