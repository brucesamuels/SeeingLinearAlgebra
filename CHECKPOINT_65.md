# Checkpoint 65 — Special Vectors

## Purpose

Create a standalone lesson introducing two special kinds of vectors:

- the unique zero vector;
- the infinitely many unit vectors.

The lesson motivates normalization geometrically before it is integrated into
the combined Chapter 1 presentation.

## Approved example

\[
\mathbf v=(3,2),
\qquad
\|\mathbf v\|=\sqrt{13}.
\]

The corresponding unit vector is

\[
\widehat{\mathbf v}
=
\frac{\mathbf v}{\|\mathbf v\|}
=
\frac1{\sqrt{13}}
\begin{bmatrix}
3\\2
\end{bmatrix}
=
\begin{bmatrix}
3/\sqrt{13}\\
2/\sqrt{13}
\end{bmatrix}.
\]

Its magnitude is

\[
\|\widehat{\mathbf v}\|=1.
\]

## Pedagogical sequence

1. Introduce two special kinds of vectors.
2. Shrink a familiar vector to the zero vector.
3. Restore \(\mathbf v=(3,2)\) and recall its magnitude.
4. Ask how to preserve direction while making the length one.
5. Divide by the magnitude.
6. Animate the vector shrinking to the unit circle.
7. Rotate the unit vector to show that every point on the unit circle
   represents a unit vector.
8. Conclude: a unit vector keeps direction but standardizes length.

## Architecture

- `engine/special_vectors_lesson.py` contains renderer-independent magnitude,
  normalization, direction, and snapshot logic.
- `scenes/special_vectors_presentation.py` is the standalone Manim lesson.
- Chapter 1 ordering is deliberately unchanged in this checkpoint.
- Integration follows only after visual approval.

## Validation

```zsh
./scripts/check_special_vectors_lesson.zsh
./scripts/render_special_vectors_presentation.zsh
```

Do not commit until the standalone render has been visually approved.
