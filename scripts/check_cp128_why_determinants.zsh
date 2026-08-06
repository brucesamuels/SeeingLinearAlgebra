#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/determinant_need.py \
  scenes/why_determinants_presentation.py \
  tests/test_determinant_need.py \
  tests/test_why_determinants_presentation.py

python -m pytest -q \
  tests/test_determinant_need.py \
  tests/test_why_determinants_presentation.py

python - <<'PY'
from engine.determinant_need import build_examples

expected = {"expand": 2.0, "contract": 0.5, "reverse": -1.0, "collapse": 0.0}
actual = {example.key: example.signed_scale for example in build_examples()}
assert actual == expected, (actual, expected)
print("CP128 mathematical smoke check passed.")
PY

if command -v manim >/dev/null 2>&1; then
  manim --version
  python - <<'PY'
from manim import Arrow, Axes, MathTex, Matrix, Polygon
print("CP128 Manim runtime-name check passed.")
PY
else
  print "Manim is not on PATH; source and mathematical checks passed, runtime import check skipped."
fi
