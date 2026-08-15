#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/gram_schmidt_three_vectors.py \
  scenes/gram_schmidt_three_vectors_presentation.py \
  tests/test_gram_schmidt_three_vectors.py \
  tests/test_gram_schmidt_three_vectors_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_gram_schmidt_three_vectors.py \
  tests/test_gram_schmidt_three_vectors_presentation.py

PYTHONPATH=. python - <<'PY'
from scenes.gram_schmidt_three_vectors_presentation import GramSchmidtThreeVectorsPresentation

assert GramSchmidtThreeVectorsPresentation.SCENE_REVISION == "cp159_r6_card5_pairwise_views"
print("CP159 runtime verification passed.")
PY
