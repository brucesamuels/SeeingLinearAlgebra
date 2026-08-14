#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m py_compile \
  engine/gram_schmidt_two_vectors.py \
  scenes/gram_schmidt_two_vectors_presentation.py \
  tests/test_gram_schmidt_two_vectors.py \
  tests/test_gram_schmidt_two_vectors_presentation.py

PYTHONPATH=. python -m pytest -q \
  tests/test_gram_schmidt_two_vectors.py \
  tests/test_gram_schmidt_two_vectors_presentation.py

PYTHONPATH=. python - <<'PY'
from scenes.gram_schmidt_two_vectors_presentation import GramSchmidtTwoVectorsPresentation

assert GramSchmidtTwoVectorsPresentation.SCENE_REVISION == "cp157_r6_card2_marker_natural_quadrant"
print("CP157 runtime verification passed.")
PY
