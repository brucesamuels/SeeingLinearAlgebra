#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m manim -pql --disable_caching \
    scenes/full_rank_linear_combination_3d_presentation.py \
    FullRankLinearCombination3DPresentation
