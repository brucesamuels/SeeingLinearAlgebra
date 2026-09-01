#!/bin/zsh
set -euo pipefail

bundle_root="${0:A:h}"
target_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${1:-$(pwd)}}"
files=(
  scenes/positive_definite_matrices_title_card.py
  scripts/build_cp213_positive_definite_preview.py
  tests/test_positive_definite_matrices_title_card.py
  tests/test_cp213_positive_definite_preview_assembly.py
  scripts/check_cp213_positive_definite_preview.zsh
  scripts/render_cp213_positive_definite_preview.zsh
  CHECKPOINT_213.md
)

[[ -d "$target_root/scenes" && -d "$target_root/scripts" ]] || {
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
  "$target_root/scripts/build_cp213_positive_definite_preview.py" \
  "$target_root/scripts/check_cp213_positive_definite_preview.zsh" \
  "$target_root/scripts/render_cp213_positive_definite_preview.zsh"

print -- "Checkpoint 213 installed in $target_root"
print -- "Activate seeingla-manim021, then run scripts/check_cp213_positive_definite_preview.zsh"
