# Checkpoint 72.1 — Installer Correction

## Problem
The original CP72 installer used a wildcard copy for each package directory. Because the downloaded package contained generated `__pycache__` directories, `cp` encountered a directory and stopped before installing the scripts.

## Correction
- Copies each intended CP72 source, scene, test, and script explicitly.
- Excludes all cache directories and compiled Python files.
- Marks the check and render scripts executable after copying.
- Safely overwrites any files that may have been partially copied by the original installer.

## Visual and mathematical impact
None. CP72.1 changes only installation reliability.
