# Checkpoint 80.4 — Import ORIGIN for Grouped Label Alignment

## Fix
CP80.3 grouped the input/output labels with `aligned_edge=ORIGIN` but did not import `ORIGIN` from Manim.

This hotfix adds the missing import and preserves all CP80.3 layout changes.

## Files updated
- `scenes/fundamental_subspaces_presentation.py`
- `tests/test_fundamental_subspaces_presentation.py`
- `CHECKPOINT_80_4.md`
