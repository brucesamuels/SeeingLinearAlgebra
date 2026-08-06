#!/bin/zsh
set -euo pipefail

repo_root="${0:A:h:h}"
cd "$repo_root"

quality="${1:--pql}"
scene="WhyDeterminantsPresentation"
source_file="scenes/why_determinants_presentation.py"

PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}" \
  manim "$quality" --disable_caching "$source_file" "$scene"

print
print "Rendered CP128. Search under media/videos/why_determinants_presentation/ for the MP4."
