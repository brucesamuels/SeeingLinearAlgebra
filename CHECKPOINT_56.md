# Checkpoint 56 — Vector Addition

## Objective

Add a standalone lesson that introduces vector addition through the
head-to-tail rule before the lesson is integrated into Chapter 1.

The scene uses

\[
\mathbf u=(3,1),
\qquad
\mathbf v=(1,2),
\qquad
\mathbf u+\mathbf v=(4,3).
\]

## Pedagogical sequence

1. Show both vectors in standard position.
2. Ask where the tail of the second vector should begin.
3. Translate \(\mathbf v\) so its tail reaches the tip of \(\mathbf u\).
4. Draw the resultant from the origin to the final endpoint.
5. Compute the coordinate sum.
6. Reveal the parallelogram only after head-to-tail addition is established.
7. Conclude that vector addition combines successive displacements.

## Architecture

`VectorAddition` is a renderer-independent specialization of the existing
`LinearCombination` model with coefficients `(1, 1)`.

It does not duplicate vector arithmetic. It derives:

- the two input vectors,
- the result,
- both tip-to-tail term segments,
- and the resultant segment

from the established `LinearCombinationSnapshot`.

The Manim scene is a thin educational adapter over that snapshot. It owns only
screen layout, labels, animation sequencing, and pacing.

## Added files

- `engine/vector_addition.py`
- `engine/vector_addition_lesson.py`
- `scenes/vector_addition_presentation.py`
- `tests/test_vector_addition.py`
- `tests/test_vector_addition_lesson.py`
- `tests/test_vector_addition_presentation.py`
- `scripts/check_vector_addition.zsh`
- `scripts/render_vector_addition_presentation.zsh`
- `CHECKPOINT_56.md`

No existing engine, scene, chapter-sequence, test, or script file is modified.

## Verification

```zsh
./scripts/check_vector_addition.zsh
```

## Render

```zsh
./scripts/render_vector_addition_presentation.zsh
```

## Next step

After visual approval, the next checkpoint should integrate the approved
Vector Addition lesson into the Chapter 1 sequence after standard position.
