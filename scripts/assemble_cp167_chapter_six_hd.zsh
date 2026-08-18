#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

for command_name in python ffmpeg ffprobe; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    print -u2 -- "CP167 HD assembly requires '$command_name' on PATH."
    exit 1
  fi
done

# Final Chapter 6 sequence, approved in the CP166 preview.
lessons=(
  '149|Why Orthogonality?|scenes/why_orthogonality_presentation.py|WhyOrthogonalityPresentation'
  '150|Dot Product and Perpendicularity|scenes/dot_product_perpendicularity_presentation.py|DotProductPerpendicularityPresentation'
  '151|Orthogonal Sets|scenes/orthogonal_sets_presentation.py|OrthogonalSetsPresentation'
  '152|Orthonormal Sets|scenes/orthonormal_sets_presentation.py|OrthonormalSetsPresentation'
  '153|Projection onto a Vector|scenes/vector_projection_presentation.py|VectorProjectionPresentation'
  '154|Orthogonal Decomposition|scenes/orthogonal_decomposition_presentation.py|OrthogonalDecompositionPresentation'
  '155|Projection onto a Subspace|scenes/subspace_projection_presentation.py|SubspaceProjectionPresentation'
  '156|Orthogonal Complements|scenes/orthogonal_complements_presentation.py|OrthogonalComplementsPresentation'
  '157|Gram-Schmidt with Two Vectors|scenes/gram_schmidt_two_vectors_presentation.py|GramSchmidtTwoVectorsPresentation'
  '159|Gram-Schmidt in R^3|scenes/gram_schmidt_three_vectors_presentation.py|GramSchmidtThreeVectorsPresentation'
  '158|From Orthogonal to Orthonormal|scenes/orthonormalization_presentation.py|OrthonormalizationPresentation'
  '160|QR Factorization: Gram-Schmidt in Matrix Form|scenes/qr_factorization_presentation.py|QRFactorizationPresentation'
  '161|Least Squares: Projection and the Normal Equation|scenes/least_squares_projection_presentation.py|LeastSquaresProjectionPresentation'
  '162|Orthogonal Matrices Preserve Geometry|scenes/orthogonal_matrices_presentation.py|OrthogonalMatricesPresentation'
  '163|Rotations and Reflections: Orthogonal Transformations|scenes/rotations_reflections_presentation.py|RotationsReflectionsPresentation'
  '164|Projection Matrices: Symmetric and Idempotent|scenes/projection_matrices_presentation.py|ProjectionMatricesPresentation'
  '165|Orthogonality and Projection: The Big Picture|scenes/chapter_six_finale_presentation.py|ChapterSixFinalePresentation'
)

output="media/ChapterSixOrthogonalityAndProjection.mp4"
work_dir="media/chapter_six_assembly_hd"
manifest="$work_dir/concat_manifest.txt"
mkdir -p "$work_dir"
: > "$manifest"

probe_spec() {
  ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
    -of csv=p=0 \
    "$1"
}

baseline_spec=""
index=0

print -- "CP167 Chapter 6 HD assembly"
print -- "---------------------------"
print -- "Fresh render target: 1080p60 (-qh)"
print -- "Final output: $output"
print -- ""

for entry in "${lessons[@]}"; do
  fields=("${(@s:|:)entry}")
  cp_number="${fields[1]}"
  lesson_title="${fields[2]}"
  scene_file="${fields[3]}"
  scene_class="${fields[4]}"
  (( index += 1 ))

  if [[ ! -f "$scene_file" ]]; then
    print -u2 -- "Missing approved scene source: $scene_file"
    exit 1
  fi

  render_name="CH6HD_${(l:2::0:)index}_CP${cp_number}_${scene_class}"
  print -- "[$index/${#lessons[@]}] Render CP$cp_number - $lesson_title"
  python -m manim --disable_caching -qh -o "$render_name" "$scene_file" "$scene_class"

  clip_file="$(find media/videos -type f -path '*/1080p60/*' -name "${render_name}.mp4" -print -quit 2>/dev/null || true)"
  if [[ -z "$clip_file" ]]; then
    print -u2 -- "Could not locate 1080p60 render for CP$cp_number after Manim completed."
    exit 1
  fi

  current_spec="$(probe_spec "$clip_file")"
  if [[ -z "$baseline_spec" ]]; then
    baseline_spec="$current_spec"
  elif [[ "$current_spec" != "$baseline_spec" ]]; then
    print -u2 -- "Video format mismatch at CP$cp_number:"
    print -u2 -- "  expected: $baseline_spec"
    print -u2 -- "  found:    $current_spec"
    exit 1
  fi

  clip_abs="${clip_file:A}"
  print -r -- "file '$clip_abs'" >> "$manifest"
done

print -- ""
print -- "Concatenating ${#lessons[@]} fresh 1080p60 lesson clips..."
ffmpeg -y -v warning \
  -f concat -safe 0 -i "$manifest" \
  -c copy -movflags +faststart \
  "$output"

output_spec="$(probe_spec "$output")"
duration="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$output")"
size="$(du -h "$output" | awk '{print $1}')"

print -- ""
print -- "Chapter 6 HD master assembled successfully."
print -- "Output:   $output"
print -- "Video:    $output_spec"
printf 'Duration: %.1f minutes\n' "$(( duration / 60.0 ))"
print -- "Size:     $size"
print -- "Open with: open '$output'"
