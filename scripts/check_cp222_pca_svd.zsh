#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP222 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP222 requires Manim Community v0.21.0."
  exit 1
}

python -m py_compile \
  engine/pca_svd.py \
  scenes/pca_svd_presentation.py
python -m pytest -q \
  tests/test_pca_svd.py \
  tests/test_pca_svd_presentation.py

print -- "Checkpoint 222 checks passed on Python 3.12 / Manim 0.21.0."
