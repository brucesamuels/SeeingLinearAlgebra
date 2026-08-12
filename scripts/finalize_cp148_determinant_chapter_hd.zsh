#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  print -u2 "ffmpeg is required to assemble Chapter 5."
  exit 2
fi

scene_classes=(
  DeterminantChapterTitleCard
  WhyDeterminantsPresentation
  DeterminantAreaScalePresentation
  DeterminantOrientationPresentation
  DeterminantFormulaGeometryPresentation
  DeterminantGeometryPresentation
  DeterminantPropertiesPresentation
  DeterminantConsequencesPresentation
  DeterminantProductRulePresentation
  DeterminantTransposeRulePresentation
  DeterminantEliminationPresentation
  DeterminantBigFormulaPresentation
  DeterminantBigFormulaDerivationPresentation
  DeterminantCofactorExpansionPresentation
  DeterminantCofactorEfficiencyPresentation
  DeterminantTriangularPresentation
  DeterminantInvertibilityPresentation
  DeterminantCramersRulePresentation
  DeterminantAdjugateInversePresentation
  DeterminantJacobianPreviewPresentation
  DeterminantChapterSynthesisPresentation
)

print "Rendering all Chapter 5 scenes at Manim high quality (1080p60)..."

for scene_class in "${scene_classes[@]}"; do
  scene_file="$(grep -RIl --include='*.py' "class ${scene_class}" scenes | head -n 1)"
  if [[ -z "$scene_file" ]]; then
    print -u2 "Could not locate source file for ${scene_class}"
    exit 3
  fi
  print ""
  print "Rendering ${scene_class}"
  python -m manim --disable_caching -qh "$scene_file" "$scene_class"
done

print ""
print "Assembling only 1080p60 renders..."
python scripts/build_cp148_determinant_chapter.py \
  --repo-root "$repo_root" \
  --quality-dir 1080p60 \
  --output media/chapter_five_determinants/Chapter5_Determinants_Final_1080p.mp4

print ""
print "Final HD chapter:"
print "$repo_root/media/chapter_five_determinants/Chapter5_Determinants_Final_1080p.mp4"
