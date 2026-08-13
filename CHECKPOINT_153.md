# Checkpoint 153 — Projection onto a Vector

## Purpose
Make projection the geometric center of the chapter: identify the component of a vector along a chosen direction by dropping a perpendicular, then derive the projection formula from the orthogonality of the residual.

## Student-facing sequence
1. Ask what part of `x` points in the direction of `u`.
2. Drop a perpendicular from `x` to `span(u)` and identify the projection `p`.
3. Write `p = c u` and use `(x - c u) · u = 0` to derive the coefficient.
4. Present the general projection formula and the simpler unit-vector formula.
5. Work the hand-friendly example `x=(3,3)`, `u=(4,1)`.
6. End with `x = projection + residual`, with the residual perpendicular to `u`, preparing orthogonal decomposition.

## Visual intent
- Geometry leads; formulas explain what the geometry forces.
- The perpendicular drop is animated deliberately and marked with a visible right-angle corner.
- The worked example uses a split layout: geometry at left, arithmetic at right.
- Pacing retains the slower transition/hold times approved in CP152.

## Engine
`engine/vector_projection.py` owns numerical projection, coefficient, residual, reconstruction, and validation.

## Preview
`CP153_r1_geometric_projection_preview.mp4`


## r2 hotfix
- Fixed the worked-example render failure by importing Manim's `LEFT` direction constant, which is used to place the example axes.
- Added a regression test so every direction constant used in that placement is explicitly present in the Manim import block.
- No lesson content, geometry, or pacing changed.
