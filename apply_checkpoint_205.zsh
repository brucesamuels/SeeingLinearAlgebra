#!/bin/zsh
set -euo pipefail

bundle_root="${0:A:h}"
target_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${1:-$(pwd)}}"
files=(
  engine/gram_matrix_definiteness.py
  scenes/gram_matrix_definiteness_presentation.py
  tests/test_gram_matrix_definiteness.py
  tests/test_gram_matrix_definiteness_presentation.py
  scripts/check_cp205_gram_matrix_definiteness.zsh
  scripts/render_cp205_gram_matrix_definiteness.zsh
  CHECKPOINT_205.md
)

[[ -d "$target_root/engine" && -d "$target_root/scenes" ]] || {
  print -u2 -- "Target is not a SeeingLinearAlgebra repository: $target_root"
  exit 1
}

for relative_path in $files; do
  source_path="$bundle_root/$relative_path"
  target_path="$target_root/$relative_path"
  [[ -f "$source_path" ]] || {
    print -u2 -- "Checkpoint bundle is missing: $relative_path"
    exit 1
  }
  if [[ "$source_path" != "$target_path" ]]; then
    mkdir -p "${target_path:h}"
    cp "$source_path" "$target_path"
  fi
done

chmod +x \
  "$target_root/scripts/check_cp205_gram_matrix_definiteness.zsh" \
  "$target_root/scripts/render_cp205_gram_matrix_definiteness.zsh"

print -- "Checkpoint 205 installed in $target_root"
print -- "Activate seeingla-manim021, then run scripts/check_cp205_gram_matrix_definiteness.zsh"
