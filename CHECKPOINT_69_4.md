# Checkpoint 69.4 — Perspective Plane Reveal

## Goal
Refine the ending of the Chapter 2 two-vector span lesson so the completed span reads as a **plane**, not as a background color change.

## What changed
- Preserved the approved one-line and moving-family construction.
- Preserved the sparse and dense endpoint-field phases.
- Replaced the flat solid-plane ending with a **restrained perspective plane reveal**.
- Built the perspective surface from the same span corners used in earlier revisions.
- Added two low-opacity outer layers to soften the perimeter.
- Added a light internal mesh so the surface reads as a geometric plane rather than a flat screen fill.
- Kept the generator vectors and moving combination visually above the plane.

## Visual intention
The construction remains entirely 2D while the span is being built:
1. one line is traced,
2. that line sweeps through the plane,
3. reachable endpoints accumulate,
4. the collection resolves into a slightly tilted plane patch.

The slight tilt is a visual cue only. It is intended to help students perceive a surface while still understanding that the underlying mathematics is a 2D span.

## Files updated
- `scenes/two_vector_span_presentation.py`
- `tests/test_two_vector_span_presentation.py`
- `CHECKPOINT_69_4.md`

## Notes
This checkpoint is additive with respect to the project history and does not modify any approved Chapter 1 scenes or mathematics engine files.
