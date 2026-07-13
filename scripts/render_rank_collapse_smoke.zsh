#!/bin/zsh
set -e

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -pql \
  examples/rank_collapse_point_cloud_smoke.py \
  RankCollapsePointCloudSmoke
