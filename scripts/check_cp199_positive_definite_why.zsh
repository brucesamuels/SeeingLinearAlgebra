#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP199 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP199 requires Manim Community v0.21.0."
  exit 1
}

python -m py_compile \
  engine/positive_definite_directional_energy.py \
  scenes/positive_definite_why_presentation.py
python -m pytest -q \
  tests/test_positive_definite_directional_energy.py \
  tests/test_positive_definite_why_presentation.py

print -- "Checkpoint 199 checks passed on Python 3.12 / Manim 0.21.0."
