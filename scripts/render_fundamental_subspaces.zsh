#!/bin/zsh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"
python -m manim --disable_caching -pql scenes/fundamental_subspaces_presentation.py FundamentalSubspacesPresentation
