#!/bin/zsh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"

QUALITY="${1:--pql}"
DURATION_FACTOR="${2:-1.25}"
BUILD_DIR="$REPO_DIR/media/chapter_build/vector_spaces"
MEDIA_DIR="$BUILD_DIR/media"
CONCAT_FILE="$BUILD_DIR/concat.txt"
OUTPUT_DIR="$REPO_DIR/media/videos/vector_spaces_chapter/480p15"
OUTPUT_FILE="$OUTPUT_DIR/VectorSpacesAndSubspacesChapter.mp4"

required_files=(
  scenes/vector_spaces_chapter_cards.py
  scenes/rank_collapse_3d_presentation.py
  scenes/subspace_test_presentation.py
  scenes/basis_dimension_presentation.py
  scenes/column_space_presentation.py
  scenes/null_space_presentation.py
  scenes/row_space_presentation.py
  scenes/pivot_columns_presentation.py
  scenes/rank_nullity_presentation.py
  scenes/fundamental_subspaces_presentation.py
)

for relative in $required_files; do
  if [[ ! -f "$REPO_DIR/$relative" ]]; then
    print -u2 -- "Missing chapter scene: $relative"
    exit 1
  fi
done

rm -rf "$BUILD_DIR"
mkdir -p "$MEDIA_DIR" "$OUTPUT_DIR"

print -- "Rendering chapter cards..."
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" \
  scenes/vector_spaces_chapter_cards.py \
  VectorSpacesChapterOpening \
  VectorSpacesSectionOne \
  VectorSpacesSectionTwo \
  VectorSpacesSectionThree \
  VectorSpacesSectionFour \
  VectorSpacesChapterClosing

print -- "Rendering chapter lessons..."
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/rank_collapse_3d_presentation.py RankCollapse3DPresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/subspace_test_presentation.py SubspaceTestPresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/basis_dimension_presentation.py BasisDimensionPresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/column_space_presentation.py ColumnSpacePresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/null_space_presentation.py NullSpacePresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/row_space_presentation.py RowSpacePresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/pivot_columns_presentation.py PivotColumnsPresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/rank_nullity_presentation.py RankNullityPresentation
python -m manim --disable_caching "$QUALITY" --media_dir "$MEDIA_DIR" scenes/fundamental_subspaces_presentation.py FundamentalSubspacesPresentation

video_path() {
  local file_stem="$1"
  local scene_name="$2"
  print -- "$MEDIA_DIR/videos/$file_stem/480p15/$scene_name.mp4"
}

segments=(
  "$(video_path vector_spaces_chapter_cards VectorSpacesChapterOpening)"
  "$(video_path vector_spaces_chapter_cards VectorSpacesSectionOne)"
  "$(video_path rank_collapse_3d_presentation RankCollapse3DPresentation)"
  "$(video_path subspace_test_presentation SubspaceTestPresentation)"
  "$(video_path vector_spaces_chapter_cards VectorSpacesSectionTwo)"
  "$(video_path basis_dimension_presentation BasisDimensionPresentation)"
  "$(video_path vector_spaces_chapter_cards VectorSpacesSectionThree)"
  "$(video_path column_space_presentation ColumnSpacePresentation)"
  "$(video_path null_space_presentation NullSpacePresentation)"
  "$(video_path row_space_presentation RowSpacePresentation)"
  "$(video_path pivot_columns_presentation PivotColumnsPresentation)"
  "$(video_path vector_spaces_chapter_cards VectorSpacesSectionFour)"
  "$(video_path rank_nullity_presentation RankNullityPresentation)"
  "$(video_path fundamental_subspaces_presentation FundamentalSubspacesPresentation)"
  "$(video_path vector_spaces_chapter_cards VectorSpacesChapterClosing)"
)

: > "$CONCAT_FILE"
for segment in $segments; do
  if [[ ! -f "$segment" ]]; then
    print -u2 -- "Expected rendered segment not found: $segment"
    exit 1
  fi
  escaped="${segment//\'/\'\\\'\'}"
  print -- "file '$escaped'" >> "$CONCAT_FILE"
done

print -- "Assembling chapter at ${DURATION_FACTOR}x duration..."
if [[ "$DURATION_FACTOR" != "1" && "$DURATION_FACTOR" != "1.0" ]]; then
  print -- "Using the Python/PyAV assembler so the chapter can be slowed without rerendering scenes."
  python scripts/assemble_vector_spaces_chapter.py "$CONCAT_FILE" "$OUTPUT_FILE" --duration-factor "$DURATION_FACTOR"
elif command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$OUTPUT_FILE"
else
  print -- "System ffmpeg not found; using the Python/PyAV assembler."
  python scripts/assemble_vector_spaces_chapter.py "$CONCAT_FILE" "$OUTPUT_FILE" --duration-factor "$DURATION_FACTOR"
fi

print -- ""
print -- "Chapter render complete:"
print -- "$OUTPUT_FILE"
