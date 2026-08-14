#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/orthonormalization.py \
  scenes/orthonormalization_presentation.py \
  tests/test_orthonormalization.py \
  tests/test_orthonormalization_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_orthonormalization.py \
  tests/test_orthonormalization_presentation.py

PYTHONPATH=. python - <<'PY'
from scenes.orthonormalization_presentation import OrthonormalizationPresentation

assert OrthonormalizationPresentation.SCENE_REVISION == "cp158_r3_grid_on_all_graphic_cards"
print("CP158 runtime verification passed.")
PY
