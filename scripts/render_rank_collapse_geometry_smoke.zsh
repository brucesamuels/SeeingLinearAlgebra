#!/bin/zsh
set -euo pipefail

script_dir=${0:A:h}
repo_root=${script_dir:h}

cd "$repo_root"

export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -ql \
  scenes/rank_collapse_geometry_smoke.py \
  RankCollapseGeometrySmoke
