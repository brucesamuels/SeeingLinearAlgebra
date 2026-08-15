#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/qr_factorization.py \
  scenes/qr_factorization_presentation.py \
  tests/test_qr_factorization.py \
  tests/test_qr_factorization_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_qr_factorization.py \
  tests/test_qr_factorization_presentation.py

PYTHONPATH=. python - <<'PY'
from scenes.qr_factorization_presentation import QRFactorizationPresentation

assert QRFactorizationPresentation.SCENE_REVISION == "cp160_r4_right_title_clearance"
print("CP160 runtime verification passed.")
PY
