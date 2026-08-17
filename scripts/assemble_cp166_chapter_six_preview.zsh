#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

fresh=0
for arg in "$@"; do
  case "$arg" in
    --fresh)
      fresh=1
      ;;
    *)
      print -u2 -- "Unknown option: $arg"
      print -u2 -- "Usage: zsh scripts/assemble_cp166_chapter_six_preview.zsh [--fresh]"
      exit 2
      ;;
  esac
done

for command_name in python ffmpeg ffprobe; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    print -u2 -- "CP166 assembly requires '$command_name' on PATH."
    exit 1
  fi
done

# Order chosen for the preview chapter.  CP159 precedes CP158 so the
# orthonormalization lesson becomes the direct conceptual bridge into QR.
lessons=(
  '149|Why Orthogonality?|scenes/why_orthogonality_presentation.py|WhyOrthogonalityPresentation|WhyOrthogonalityPresentation'
  '150|Dot Product and Perpendicularity|scenes/dot_product_perpendicularity_presentation.py|DotProductPerpendicularityPresentation|CP150_r6_verified_preview'
  '151|Orthogonal Sets|scenes/orthogonal_sets_presentation.py|OrthogonalSetsPresentation|CP151_r14_expanded_3d_rotation_preview'
  '152|Orthonormal Sets|scenes/orthonormal_sets_presentation.py|OrthonormalSetsPresentation|CP152_r2_slower_transitions_preview'
  '153|Projection onto a Vector|scenes/vector_projection_presentation.py|VectorProjectionPresentation|CP153_r2_left_import_hotfix_preview'
  '154|Orthogonal Decomposition|scenes/orthogonal_decomposition_presentation.py|OrthogonalDecompositionPresentation|CP154_r2_labeled_geometry_preview'
  '155|Projection onto a Subspace|scenes/subspace_projection_presentation.py|SubspaceProjectionPresentation|CP155_r4_card3_spacing_preview'
  '156|Orthogonal Complements|scenes/orthogonal_complements_presentation.py|OrthogonalComplementsPresentation|CP156_r22_card4_caption_left_and_raise_preview'
  '157|Gram-Schmidt with Two Vectors|scenes/gram_schmidt_two_vectors_presentation.py|GramSchmidtTwoVectorsPresentation|CP157_r6_card2_marker_natural_quadrant_preview'
  '159|Gram-Schmidt in R^3|scenes/gram_schmidt_three_vectors_presentation.py|GramSchmidtThreeVectorsPresentation|CP159_r6_card5_pairwise_views_preview'
  '158|From Orthogonal to Orthonormal|scenes/orthonormalization_presentation.py|OrthonormalizationPresentation|CP158_r3_grid_on_all_graphic_cards_preview'
  '160|QR Factorization: Gram-Schmidt in Matrix Form|scenes/qr_factorization_presentation.py|QRFactorizationPresentation|CP160_r4_right_title_clearance_preview'
  '161|Least Squares: Projection and the Normal Equation|scenes/least_squares_projection_presentation.py|LeastSquaresProjectionPresentation|CP161_r14_lower_penultimate_math_blocks_preview'
  '162|Orthogonal Matrices Preserve Geometry|scenes/orthogonal_matrices_presentation.py|OrthogonalMatricesPresentation|OrthogonalMatricesPresentation'
  '163|Rotations and Reflections: Orthogonal Transformations|scenes/rotations_reflections_presentation.py|RotationsReflectionsPresentation|RotationsReflectionsPresentation'
  '164|Projection Matrices: Symmetric and Idempotent|scenes/projection_matrices_presentation.py|ProjectionMatricesPresentation|ProjectionMatricesPresentation'
  '165|Orthogonality and Projection: The Big Picture|scenes/chapter_six_finale_presentation.py|ChapterSixFinalePresentation|ChapterSixFinalePresentation'
)

output="media/ChapterSixOrthogonalityAndProjection_preview.mp4"
work_dir="media/chapter_six_assembly_preview"
manifest="$work_dir/concat_manifest.txt"
mkdir -p "$work_dir"
: > "$manifest"

find_existing_clip() {
  local preferred_name="$1"
  local scene_class="$2"
  local found=""

  if [[ ! -d media/videos ]]; then
    return 1
  fi

  found="$(find media/videos -type f -path '*/480p15/*' -name "${preferred_name}.mp4" -print -quit 2>/dev/null || true)"
  if [[ -z "$found" && "$preferred_name" != "$scene_class" ]]; then
    found="$(find media/videos -type f -path '*/480p15/*' -name "${scene_class}.mp4" -print -quit 2>/dev/null || true)"
  fi

  [[ -n "$found" ]] || return 1
  print -r -- "$found"
}

probe_spec() {
  ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
    -of csv=p=0 \
    "$1"
}

clip_paths=()
baseline_spec=""
index=0

print -- "CP166 Chapter 6 preview assembly"
print -- "-----------------------------------"

for entry in "${lessons[@]}"; do
  fields=("${(@s:|:)entry}")
  cp_number="${fields[1]}"
  lesson_title="${fields[2]}"
  scene_file="${fields[3]}"
  scene_class="${fields[4]}"
  preferred_name="${fields[5]}"
  (( index += 1 ))

  if [[ ! -f "$scene_file" ]]; then
    print -u2 -- "Missing approved scene source: $scene_file"
    exit 1
  fi

  clip_file=""
  if (( fresh == 0 )); then
    clip_file="$(find_existing_clip "$preferred_name" "$scene_class" || true)"
  fi

  if [[ -n "$clip_file" ]]; then
    print -- "[$index/${#lessons[@]}] Reuse CP$cp_number - $lesson_title"
  else
    render_name="CH6_${(l:2::0:)index}_CP${cp_number}_${scene_class}"
    print -- "[$index/${#lessons[@]}] Render CP$cp_number - $lesson_title"
    python -m manim --disable_caching -ql -o "$render_name" "$scene_file" "$scene_class"
    clip_file="$(find media/videos -type f -path '*/480p15/*' -name "${render_name}.mp4" -print -quit 2>/dev/null || true)"
    if [[ -z "$clip_file" ]]; then
      print -u2 -- "Could not locate rendered clip for CP$cp_number after Manim completed."
      exit 1
    fi
  fi

  current_spec="$(probe_spec "$clip_file")"
  if [[ -z "$baseline_spec" ]]; then
    baseline_spec="$current_spec"
  elif [[ "$current_spec" != "$baseline_spec" ]]; then
    print -u2 -- "Video format mismatch at CP$cp_number:"
    print -u2 -- "  expected: $baseline_spec"
    print -u2 -- "  found:    $current_spec"
    print -u2 -- "Re-run with --fresh to render a uniform 480p15 preview set."
    exit 1
  fi

  clip_abs="${clip_file:A}"
  print -r -- "file '$clip_abs'" >> "$manifest"
  clip_paths+=("$clip_file")
done

print -- ""
print -- "Concatenating ${#clip_paths[@]} approved lesson clips..."
ffmpeg -y -v warning \
  -f concat -safe 0 -i "$manifest" \
  -c copy -movflags +faststart \
  "$output"

output_spec="$(probe_spec "$output")"
duration="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$output")"

print -- ""
print -- "Chapter 6 preview assembled successfully."
print -- "Output: $output"
print -- "Video:  $output_spec"
printf 'Duration: %.1f minutes\n' "$(( duration / 60.0 ))"
print -- "Open with: open '$output'"
