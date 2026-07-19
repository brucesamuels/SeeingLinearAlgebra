# Checkpoint 61 — Vector Subtraction as Adding a Negative

## Objective

Introduce vector subtraction through the identity

\[
\mathbf u-\mathbf v=\mathbf u+(-\mathbf v).
\]

The lesson reuses

\[
\mathbf u=(3,1),
\qquad
\mathbf v=(1,2),
\]

so that

\[
-\mathbf v=(-1,-2),
\qquad
\mathbf u-\mathbf v=(2,-1).
\]

## Pedagogical sequence

1. Show \(\mathbf u\) and \(\mathbf v\) in standard position.
2. Ask how subtraction can be drawn using addition alone.
3. Rotate \(\mathbf v\) through the origin to form \(-\mathbf v\).
4. Emphasize that the negative vector preserves magnitude and reverses
   direction.
5. Translate \(-\mathbf v\) to the tip of \(\mathbf u\).
6. Draw the resultant and complete the coordinate calculation.
7. Conclude: **To subtract a vector, add its opposite.**

## Architecture

CP61 adds a renderer-independent `VectorSubtraction` model backed by the
existing `LinearCombination` pipeline at coefficients `(1, -1)`.

The snapshot exposes the original vectors, the negative vector, head-to-tail
segments, the resultant, and instructional invariants. The Manim scene owns
only layout, animation, labels, and pacing.

## Added files

- `engine/vector_subtraction.py`
- `engine/vector_subtraction_lesson.py`
- `scenes/vector_subtraction_presentation.py`
- `tests/test_vector_subtraction.py`
- `tests/test_vector_subtraction_lesson.py`
- `tests/test_vector_subtraction_presentation.py`
- `scripts/check_vector_subtraction.zsh`
- `scripts/render_vector_subtraction_presentation.zsh`
- `CHECKPOINT_61.md`

No Chapter 1 ordering file is modified.

## Verification

```zsh
./scripts/check_vector_subtraction.zsh
```

## Render

```zsh
./scripts/render_vector_subtraction_presentation.zsh
```

## Next step

After visual approval, CP62 can integrate the commutativity and subtraction
lessons into the Chapter 1 sequence before the three-vector 3D extension.
