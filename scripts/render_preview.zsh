#!/bin/zsh
set -e
cd "${0:A:h}/.."
python3 -m manim -pql episode01_vectors/episode01.py Episode01Vectors
python3 -m manim -pql episode02_subspaces/episode02.py Episode02Subspaces
