#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP213 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP213 requires Manim Community v0.21.0."
  exit 1
}
for command_name in ffmpeg ffprobe; do
  command -v "$command_name" >/dev/null 2>&1 || {
    print -u2 -- "CP213 requires $command_name."
    exit 1
  }
done

python -m py_compile \
  scenes/positive_definite_matrices_title_card.py \
  scripts/build_cp213_positive_definite_preview.py
python -m pytest -q \
  tests/test_positive_definite_matrices_title_card.py \
  tests/test_cp213_positive_definite_preview_assembly.py

print -- "Checkpoint 213 checks passed on Python 3.12 / Manim 0.21.0."
