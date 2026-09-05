#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP223 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP223 requires Manim Community v0.21.0."
  exit 1
}

python -m py_compile \
  engine/svd_chapter_synthesis.py \
  scenes/svd_chapter_synthesis_presentation.py
python -m pytest -q \
  tests/test_svd_chapter_synthesis.py \
  tests/test_svd_chapter_synthesis_presentation.py

print -- "Checkpoint 223 checks passed on Python 3.12 / Manim 0.21.0."
