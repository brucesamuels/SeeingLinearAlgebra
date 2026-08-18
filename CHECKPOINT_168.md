# Seeing Linear Algebra — Checkpoint 168

## Goal

Begin Chapter 7, **Eigenvalues and Eigenvectors**, with a geometric discovery lesson:

**Why Eigenvectors? — Special Directions of a Transformation**

The checkpoint deliberately does **not** introduce the equation
`A v = lambda v`, characteristic polynomials, or determinant computation.
Students first see the geometric phenomenon that motivates the terminology.

## Revised conceptual contrast

The lesson now begins by contrasting **two different linear transformations**.
This makes the special nature of an eigenvector direction visible before the term
itself is introduced.

### Act I — a transformation with no real invariant direction

First apply a quarter-turn rotation

\[
R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
\]

Every nonzero real vector is rotated by 90 degrees, so every image lies on a line
different from its original line through the origin. The scene states explicitly:

> A 90° rotation moves every nonzero vector to a different line.
>
> No image stays on its original line.

The original dashed direction lines remain visible while the arrows rotate.

### Act II — a transformation with two invariant directions

The same arrows are reset to their starting positions. The matrix is then replaced
by

\[
A=\begin{bmatrix}3&1\\1&3\end{bmatrix}.
\]

The same collection of vectors is transformed again. Four images leave their
original lines, but two directions remain on their original lines:

\[
y=x, \qquad y=-x.
\]

The generic vectors fade back and the two invariant lines are highlighted. Only
then does the scene introduce:

> These special directions are eigenvector directions.

The hidden scale factors 4 and 2 are still verified in the renderer-independent
engine tests but are intentionally deferred to the next lesson.

## Revised visual sequence

1. Chapter banner and yellow lesson title.
2. Ask: “Do any directions stay on their original lines?”
3. Fixed coordinate grid, six arrows, and dashed original lines.
4. Display the 90-degree rotation matrix.
5. Animate all six arrows through the quarter-turn.
6. Hold the result against the original dashed lines.
7. State that no image stays on its original line.
8. Reset the same arrows to their original positions.
9. Replace the rotation matrix with the symmetric matrix.
10. Apply the second transformation to exactly the same vectors.
11. Hold again for comparison with the original dashed lines.
12. Fade generic vectors into the background.
13. Highlight the two lines that remain invariant.
14. Label both highlighted cases “same line.”
15. Reveal the phrase **eigenvector directions**.

## Pedagogical purpose

The contrast answers the opening question visually:

- A transformation need not have any real direction that remains on its line.
- Another transformation may have special directions that do remain on their lines.
- Those surviving directions are precisely the phenomenon the chapter will study.

This is stronger than asking students to distinguish generic and special arrows
inside a single transformation because the first transformation establishes that
invariant directions are not automatic.

## Layout discipline

The scene retains:

- fixed 2D camera;
- coordinate grid behind all vector geometry;
- chapter banner and yellow lesson title in separate upper bands;
- one concise white heading at a time;
- bottom caption band separated from the geometry;
- original dashed direction lines as the persistent visual reference.

## Files

Checkpoint files:

```text
engine/eigenvector_special_directions.py
scenes/eigenvector_special_directions_presentation.py
tests/test_eigenvector_special_directions.py
tests/test_eigenvector_special_directions_presentation.py
scripts/check_cp168_eigenvector_special_directions.zsh
scripts/render_cp168_eigenvector_special_directions.zsh
CHECKPOINT_168.md
```

The render script retains the repository-root `PYTHONPATH` export required for
Manim to resolve imports from `engine` when loading the scene file directly.

## Verification

Focused tests cover:

- the quarter-turn rotation matrix;
- absence of preserved sample directions under the rotation;
- the symmetric comparison matrix;
- exactly four generic and two invariant sample directions under the second matrix;
- hidden scale factors for the two invariant directions;
- renderer-independent matrix-vector multiplication;
- zero-vector rejection;
- fixed 2D `NumberPlane` presentation;
- explicit reset of the same arrows between transformations;
- replacement of the first matrix by the second;
- delayed introduction of eigenvector terminology;
- absence of characteristic-polynomial material;
- absence of checkpoint numbers in the student-facing scene.

## Visual approval target

The preview should make this contrast obvious without narration:

> Under the 90-degree rotation, every vector leaves its original line. Under the
> second transformation, two special directions stay on their original lines.

Source tests cannot establish collision-free rendering. Visual approval of the
`-pql` preview is required before this checkpoint is committed or CP169 begins.


## Visual clarification revision

The second transformation was strengthened from `[[3, 1], [1, 3]]` to `[[5, 3], [3, 5]]`. It retains the same two invariant directions `y=x` and `y=-x`, but produces a much larger angular change for generic vectors. The presentation also now leaves a faded dashed ghost of every original vector in place throughout each transformation, in addition to the faint full reference line, so students can compare the original and transformed directions directly. A single display scale is applied to transformed endpoints in the second act only to keep the stronger map comfortably inside the coordinate grid; it does not change any displayed direction.


## Visual refinement: frozen ghost vectors and final isolation

- Original vectors now remain as frozen, faded dashed ghost references while only the live vectors transform.
- After the second transformation, the complete before/after comparison is held on screen long enough to read.
- Generic transformed vectors, their generic ghosts, and generic reference rays then fade away together, leaving only the two invariant/eigenvector directions for the final reveal.
