# Checkpoint 71.1 — Render Import-Path Correction

## Problem
Running the CP71 render script produced:

```text
ModuleNotFoundError: No module named 'engine'
```

The standalone `manim` launcher did not reliably place the repository root on Python's module search path.

## Correction
The render script now:

1. changes into the repository root,
2. exports the repository root through `PYTHONPATH`, and
3. invokes Manim with the active Python interpreter using `python -m manim`.

This keeps imports such as

```python
from engine.dimension_growth import DimensionGrowth
```

consistent with the rest of the project.

## Files updated
- `scripts/render_dimension_growth.zsh`
- `CHECKPOINT_71_1.md`

No mathematics, presentation, or rendering code is changed.
