#!/usr/bin/env zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
cd "$REPO_ROOT"

print "Running Checkpoint 16 focused tests..."
python -m pytest -q tests/test_linear_combination_trace.py

print "Running complete test suite..."
python -m pytest -q
