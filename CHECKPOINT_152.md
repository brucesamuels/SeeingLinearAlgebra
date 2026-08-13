# Checkpoint 152 — Orthonormal Sets

## Goal
Strengthen the idea of an orthogonal set by adding unit length, then show why this stronger condition makes dot products especially useful.

## Student-facing sequence
1. Orthogonality separates directions; ask what changes when every vector has length 1.
2. Define an orthonormal set and introduce the compact relation \(q_i\cdot q_j=\delta_{ij}\).
3. In 3-space, normalize three mutually orthogonal vectors without changing their directions; the right angles remain.
4. Package all pairwise dot products in the Gram matrix identity \(Q^TQ=I\).
5. Derive that for \(x=\sum c_iq_i\), orthonormality gives \(c_j=q_j\cdot x\).
6. Bridge to projection by asking how much of a vector points in one chosen unit direction, without yet giving the full projection formula.

## Visual design
- Reuse the approved CP151 3D camera family: initial \(\theta=-15^\circ\), followed by a wider sweep to make perpendicular directions legible.
- Keep the chapter banner and lesson title fixed in-frame.
- Use one 3D normalization card; the remaining cards emphasize uncluttered mathematical structure.
- Preserve separate vertical zones for heading, central mathematics/geometry, and bottom explanatory text.

## Files
- `engine/orthonormal_sets.py`
- `scenes/orthonormal_sets_presentation.py`
- `tests/test_orthonormal_sets.py`
- `tests/test_orthonormal_sets_presentation.py`
- `scripts/check_cp152_orthonormal_sets.zsh`
- `scripts/render_cp152_orthonormal_sets.zsh`

## r2 pacing refinement
- Keep all approved r1 content, layout, and camera framing unchanged.
- Slow card entrances and exits to about 1.35 seconds.
- Slow emphasis reveals to about 1.15 seconds.
- Lengthen the 3D camera sweep from 2.4 to 3.4 seconds.
- Slow vector normalization transforms from 0.65 to 0.95 seconds.
- Extend conclusion holds to roughly 2.6–3.0 seconds so students can read before the next transition.
