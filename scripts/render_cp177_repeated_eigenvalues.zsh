#!/bin/zsh
set -euo pipefail
repo_root="${0:A:h:h}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m manim -pql scenes/repeated_eigenvalues_presentation.py RepeatedEigenvaluesPresentation
