#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m manim scenes/chapter_six_finale_presentation.py ChapterSixFinalePresentation "$@"
