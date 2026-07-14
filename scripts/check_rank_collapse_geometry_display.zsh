#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"

print "Running RankCollapseGeometryDisplayAdapter tests..."
python -m pytest tests/test_rank_collapse_geometry_display.py -q

print "Running complete test suite..."
python -m pytest -q
