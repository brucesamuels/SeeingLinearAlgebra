#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP220 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP220 requires Manim Community v0.21.0."
  exit 1
}

python -m py_compile \
  engine/truncated_svd_approximation.py \
  scenes/truncated_svd_approximation_presentation.py
python -m pytest -q \
  tests/test_truncated_svd_approximation.py \
  tests/test_truncated_svd_approximation_presentation.py

print -- "Checkpoint 220 checks passed on Python 3.12 / Manim 0.21.0."
