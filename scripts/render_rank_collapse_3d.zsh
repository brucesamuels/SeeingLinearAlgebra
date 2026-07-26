#!/bin/zsh
set -euo pipefail
REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m manim --disable_caching -pql scenes/rank_collapse_3d_presentation.py RankCollapse3DPresentation
