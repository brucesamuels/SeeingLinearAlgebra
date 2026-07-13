#!/bin/zsh
set -e

cd "$(dirname "$0")/.."
python -m pytest -q tests/test_rank_collapse.py tests/test_rank_collapse_path.py
