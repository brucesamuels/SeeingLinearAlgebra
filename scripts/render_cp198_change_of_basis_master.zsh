#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

render_scene() {
  local source_file="$1"
  local scene_class="$2"
  print -- "Rendering 1080p60: $scene_class"
  manim --disable_caching -qh "$source_file" "$scene_class"
}

render_scene scenes/change_of_basis_title_card.py ChangeOfBasisTitleCard
render_scene scenes/why_change_basis_presentation.py WhyChangeBasisPresentation
render_scene scenes/coordinates_relative_to_basis_presentation.py CoordinatesRelativeToBasisPresentation
render_scene scenes/coordinate_linear_combinations_presentation.py CoordinateLinearCombinationsPresentation
render_scene scenes/basis_matrix_presentation.py BasisMatrixPresentation
render_scene scenes/standard_to_basis_coordinates_presentation.py StandardToBasisCoordinatesPresentation
render_scene scenes/two_basis_coordinates_presentation.py TwoBasisCoordinatesPresentation
render_scene scenes/transformation_matrix_basis_presentation.py TransformationMatrixBasisPresentation
render_scene scenes/transformation_between_bases_presentation.py TransformationBetweenBasesPresentation
render_scene scenes/good_basis_presentation.py GoodBasisPresentation
render_scene scenes/change_of_basis_review_presentation.py ChangeOfBasisReviewPresentation

python scripts/build_cp198_change_of_basis_master.py \
  --repo-root "$repo_root" \
  --quality 1080p60 \
  --speed 0.85

master="$repo_root/media/change_of_basis_master_85pct.mp4"
if [[ "$(uname -s)" == "Darwin" ]]; then
  open "$master"
else
  print -- "Classroom master ready: $master"
fi

