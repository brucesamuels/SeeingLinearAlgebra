# Checkpoint 80.3 — Keep “Input Space” and “Output Space” Clear of the Boxes

## Goal
Fix the remaining collision between the subtitle labels `input space` / `output space` and the tops of the ambient-space boxes.

## Changes
- Reorganized each ambient-space label into a two-line grouped block.
- Positioned the entire block above its box, rather than anchoring only `\mathbb R^n` / `\mathbb R^m` and letting the subtitle hang downward into the box.
- Preserved the CP80.2 fixes for the lowered boxes, raised label area, cleared dimension-summary stage, and clean final summary screen.

## Files updated
- `scenes/fundamental_subspaces_presentation.py`
- `tests/test_fundamental_subspaces_presentation.py`
- `CHECKPOINT_80_3.md`
