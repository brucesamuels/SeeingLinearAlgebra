# Checkpoint 79.2 — Enlarge the Graphic and Move Labels Off the Vectors

## Goal
Improve the readability of CP79.1 by making the geometry larger and preventing labels from obscuring the vectors.

## What changed
- Enlarged both the input-space and output-space axes.
- Expanded the row-space plane and null-space line slightly so the geometry occupies more of the screen.
- Moved the labels farther away from the vector tips and segments.
- Added dark background strokes to all spatial labels so they remain readable without covering the vectors.
- Kept the mathematical story unchanged:
  - \(\mathbf x = \mathbf x_{\mathrm{row}} + \mathbf x_{\mathrm{null}}\)
  - \(A\mathbf x = A\mathbf x_{\mathrm{row}} + \mathbf 0\)
  - \(\mathbb R^3 = \operatorname{row}(A) \oplus \operatorname{null}(A)\)

## Files updated
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_2.md`
