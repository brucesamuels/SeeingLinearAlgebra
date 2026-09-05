#!/bin/zsh
set -euo pipefail

bundle_root="${0:A:h}"
target_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${1:-$(pwd)}}"
files=(
  scenes/singular_values_rank_approximation_title_card.py
  scripts/build_cp224_svd_chapter_preview.py
  scripts/check_cp224_svd_chapter_preview.zsh
  scripts/render_cp224_svd_chapter_preview.zsh
  tests/test_singular_values_rank_approximation_title_card.py
  tests/test_cp224_svd_chapter_preview_assembly.py
  CHECKPOINT_224.md
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

cp "$bundle_root/apply_checkpoint_224.zsh" "$target_root/apply_checkpoint_224.zsh"
chmod +x \
  "$target_root/apply_checkpoint_224.zsh" \
  "$target_root/scripts/build_cp224_svd_chapter_preview.py" \
  "$target_root/scripts/check_cp224_svd_chapter_preview.zsh" \
  "$target_root/scripts/render_cp224_svd_chapter_preview.zsh"

print -- "Checkpoint 224 installed in $target_root"
print -- "Activate seeingla-manim021, then run scripts/check_cp224_svd_chapter_preview.zsh"
