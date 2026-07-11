#!/bin/zsh
set -e
echo "Checking Seeing Mathematics project..."
[[ -f "requirements.txt" ]] || { echo "ERROR: Run from project root."; exit 1; }

python3 - <<'PY'
import importlib.util
from pathlib import Path

if importlib.util.find_spec("manim") is None:
    raise SystemExit("ERROR: Manim is not installed in this Python environment.")

required = [
    Path("engine/theme.py"),
    Path("engine/branding.py"),
    Path("engine/scene_tools.py"),
    Path("tests/test_engine.py"),
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit("ERROR: Missing files:\n" + "\n".join(missing))

print("Python and project files are available.")
print("Brooklyn Tech seal found." if Path("assets/BTHSseal.jpeg").exists()
      else "NOTE: seal missing; placeholder will be used.")
PY

echo "Project check complete."
