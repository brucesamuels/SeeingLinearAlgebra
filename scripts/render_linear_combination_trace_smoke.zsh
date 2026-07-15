#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -pql \
  scenes/linear_combination_trace_smoke.py \
  LinearCombinationTraceSmoke
