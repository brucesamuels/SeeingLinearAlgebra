#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  print -u2 "ffmpeg is required to assemble Chapter 5."
  exit 2
fi

print "Rendering Chapter 5 title card..."
python -m manim --disable_caching -pql \
  scenes/determinant_chapter_title_card.py \
  DeterminantChapterTitleCard

print "Rerendering CP134 elimination lesson so the corrected banner is used..."
python -m manim --disable_caching -pql \
  scenes/determinant_elimination_presentation.py \
  DeterminantEliminationPresentation

print "Assembling newest approved lesson renders..."
python scripts/build_cp148_determinant_chapter.py --repo-root "$repo_root"

print ""
print "Chapter 5 preview assembly complete:"
print "$repo_root/media/chapter_five_determinants/Chapter5_Determinants_Assembly.mp4"
