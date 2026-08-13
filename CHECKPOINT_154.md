# Checkpoint 154 — Orthogonal Decomposition

## Goal
Turn the geometric act of projection into the broader structural idea of an orthogonal decomposition.

## Student-facing arc
1. Projection splits a vector into a component along a line and a perpendicular remainder.
2. The parallel component lies in `W`; the residual lies in `W^perp`.
3. The orthogonal split is unique.
4. A clean example uses `x=(4,2)` and `W=span(1,1)`, producing `p=(3,3)` and `r=(1,-1)`.
5. Orthogonality gives the Pythagorean identity for squared lengths.
6. The lesson closes by asking how to find the projected component when `W` has several basis vectors, setting up projection onto a subspace.

## Visual priorities
- Geometry carries the opening and numerical example.
- The decomposition is shown head-to-tail as `x = p + r`.
- A visible right-angle marker reinforces orthogonality.
- Text and equations remain in fixed vertical zones with generous margins.
- Pacing matches the slower, deliberate timing approved in the preceding lessons.

## Engine
`engine/orthogonal_decomposition.py` reuses the renderer-independent vector projection operation and owns the decomposition, orthogonality, reconstruction, and Pythagorean checks.

## Revision
`cp154_r1_orthogonal_decomposition`


## r2 visual refinement
- Labels the geometry directly rather than relying only on color.
- Adds `W` to the conceptual decomposition diagrams.
- On the numerical example, labels `x`, `p`, `r`, and places `W=span(1,1)` directly on the diagonal subspace line.
