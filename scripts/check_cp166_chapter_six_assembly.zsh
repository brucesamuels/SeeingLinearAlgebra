#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

python -m pytest -q tests/test_cp166_chapter_six_assembly.py

required_scenes=(
  scenes/why_orthogonality_presentation.py
  scenes/dot_product_perpendicularity_presentation.py
  scenes/orthogonal_sets_presentation.py
  scenes/orthonormal_sets_presentation.py
  scenes/vector_projection_presentation.py
  scenes/orthogonal_decomposition_presentation.py
  scenes/subspace_projection_presentation.py
  scenes/orthogonal_complements_presentation.py
  scenes/gram_schmidt_two_vectors_presentation.py
  scenes/gram_schmidt_three_vectors_presentation.py
  scenes/orthonormalization_presentation.py
  scenes/qr_factorization_presentation.py
  scenes/least_squares_projection_presentation.py
  scenes/orthogonal_matrices_presentation.py
  scenes/rotations_reflections_presentation.py
  scenes/projection_matrices_presentation.py
  scenes/chapter_six_finale_presentation.py
)

missing=()
for candidate_path in "${required_scenes[@]}"; do
  [[ -f "$candidate_path" ]] || missing+=("$candidate_path")
done

if (( ${#missing[@]} > 0 )); then
  print -u2 -- "CP166 assembly is missing approved scene sources:"
  for candidate_path in "${missing[@]}"; do
    print -u2 -- "  $candidate_path"
  done
  exit 1
fi

print -- "CP166 assembly checks passed: all 17 approved Chapter 6 scene sources are present."
