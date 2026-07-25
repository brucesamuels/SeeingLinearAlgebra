# Checkpoint 69.3 — Endpoint Field to Solid Plane

## Purpose

Refine the ending of the two-vector span lesson so the geometric conclusion is unmistakable.

## Visual progression

1. One fixed-coefficient line is traced.
2. Seventeen retained line positions show that the line sweeps continuously.
3. A denser first endpoint pass samples 31 coefficient-a values and 41 coefficient-b values.
4. An interleaved second pass closes the visible gaps.
5. After maximum endpoint density, a generator-aligned solid plane fades in beneath the dots.
6. The dots recede but remain faintly visible long enough to connect the sampled endpoints to the complete plane.
7. Only then is the formal definition of span revealed.

## Architectural notes

- The solid plane corners are computed through `TwoVectorSpan.endpoints_for`; they are not arbitrary screen-space decoration.
- The polygon extends well beyond the frame so the result reads as an unbounded plane.
- Approved CP69 mathematics and adapters remain unchanged.
- Chapter 1 files are untouched.

## Visual acceptance questions

- Do the additional sweep lines make the translation feel continuous?
- Does the maximum dot field clearly represent reachable endpoints?
- Does the solid reveal feel like the completion of those endpoints rather than a separate overlay?
- Do the generator and resultant vectors remain legible above the plane?
