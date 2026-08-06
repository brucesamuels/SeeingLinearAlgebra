#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

quality="${1:--pql}"
scene_file="scenes/determinant_area_scale_presentation.py"
scene_name="DeterminantAreaScalePresentation"

PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}" \
  manim "$quality" --disable_caching "$scene_file" "$scene_name"
