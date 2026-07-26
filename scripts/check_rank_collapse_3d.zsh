#!/bin/zsh
set -euo pipefail
REPO="${0:A:h:h}"
cd "$REPO"
python -m pytest -q tests/test_rank_collapse_3d.py tests/test_rank_collapse_3d_presentation.py
python -m pytest -q
