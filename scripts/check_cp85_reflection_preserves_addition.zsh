#!/bin/zsh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q   tests/test_reflection_additivity.py   tests/test_reflection_preserves_addition_presentation.py
