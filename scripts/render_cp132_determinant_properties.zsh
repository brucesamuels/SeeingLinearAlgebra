#!/bin/zsh
set -euo pipefail
repo_root="${0:A:h:h}"
cd "$repo_root"
quality="${1:--pql}"
PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}" \
  manim "$quality" --disable_caching \
  scenes/determinant_properties_presentation.py \
  DeterminantPropertiesPresentation
