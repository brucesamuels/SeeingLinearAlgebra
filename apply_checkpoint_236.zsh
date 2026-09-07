#!/bin/zsh
set -euo pipefail

bundle_root="${0:A:h}"
target_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${1:-$(pwd)}}"
files=(
  engine/graph_random_walk.py
  scenes/graph_random_walk_presentation.py
  tests/test_graph_random_walk.py
  tests/test_graph_random_walk_presentation.py
  scripts/check_cp236_graph_random_walk.zsh
  scripts/render_cp236_graph_random_walk.zsh
  CHECKPOINT_236.md
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

cp "$bundle_root/apply_checkpoint_236.zsh" "$target_root/apply_checkpoint_236.zsh"
chmod +x \
  "$target_root/apply_checkpoint_236.zsh" \
  "$target_root/scripts/check_cp236_graph_random_walk.zsh" \
  "$target_root/scripts/render_cp236_graph_random_walk.zsh"

print -- "Checkpoint 236 installed in $target_root"
print -- "Activate seeingla-manim021, then run scripts/check_cp236_graph_random_walk.zsh"

