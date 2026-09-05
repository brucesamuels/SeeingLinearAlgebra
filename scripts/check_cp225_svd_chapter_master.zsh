#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"CP225 requires Python 3.12; found {sys.version.split()[0]}")
PY
python -m manim --version | grep -q "v0.21.0" || {
  print -u2 -- "CP225 requires Manim Community v0.21.0."
  exit 1
}
for command_name in ffmpeg ffprobe; do
  command -v "$command_name" >/dev/null 2>&1 || {
    print -u2 -- "CP225 requires $command_name."
    exit 1
  }
done

python -m py_compile scripts/build_cp225_svd_chapter_master.py
python -m pytest -q tests/test_cp225_svd_chapter_master.py

print -- "Checkpoint 225 checks passed on Python 3.12 / Manim 0.21.0."
