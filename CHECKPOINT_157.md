# Checkpoint 157 - Gram-Schmidt with Two Vectors

## Purpose

Begin Gram-Schmidt by showing its first nontrivial case visually: start with two
spanning vectors, project the second onto the first, subtract that component,
and obtain a new direction perpendicular to the first.

This checkpoint keeps **projection** at the conceptual center. It treats
Gram-Schmidt not as a mysterious formula, but as the natural continuation of the
projection chapter:

\[
\text{projection} \longrightarrow \text{subtract the parallel part} \longrightarrow \text{orthogonal direction}.
\]

## Mathematical narrative

1. Start with a spanning pair `v_1, v_2`.
2. Keep the first direction: `u_1 = v_1`.
3. Compute the projection of `v_2` onto `u_1`.
4. Subtract that projection to define
   `u_2 = v_2 - \operatorname{proj}_{u_1} v_2`.
5. Verify that `u_1 \cdot u_2 = 0`.
6. State the two-vector Gram-Schmidt step and preserve the span.
7. Bridge to the next lesson: normalization to create an orthonormal set.

The concrete example is

\[
\mathbf v_1=(1,2),\qquad \mathbf v_2=(4,3),
\]

so that

\[
\operatorname{proj}_{\mathbf u_1}\mathbf v_2=(2,4),
\qquad
\mathbf u_2=(2,-1).
\]

## Files

- `engine/gram_schmidt_two_vectors.py`
- `scenes/gram_schmidt_two_vectors_presentation.py`
- `tests/test_gram_schmidt_two_vectors.py`
- `tests/test_gram_schmidt_two_vectors_presentation.py`
- `scripts/check_cp157_gram_schmidt_two_vectors.zsh`
- `scripts/render_cp157_gram_schmidt_two_vectors.zsh`
- `CHECKPOINT_157.md`

## Install

macOS Safari auto-unzips the download, so install from the extracted folder:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp157/apply_checkpoint_157.zsh
```

## Check

```zsh
zsh scripts/check_cp157_gram_schmidt_two_vectors.zsh
```

## Preview render

```zsh
zsh scripts/render_cp157_gram_schmidt_two_vectors.zsh -pql
```

The preview file is named:

```text
CP157_initial_orthogonalization_preview.mp4
```

Do not commit until the preview has been visually approved.

## Visual review notes

- The 2D plane should have equal horizontal and vertical scaling so the final
  right angle reads clearly.
- The projection card should make the parallel component visually distinct from
  the original `v_2` direction.
- The subtraction card should clearly show the residual being re-anchored at the
  origin to become `u_2`.
- The orthogonality card should use a right-angle marker and a clean dot-product
  verification.
- The summary card should feel like the first reusable Gram-Schmidt recipe,
  rather than a one-off computation.
- The bridge should point explicitly to normalization / orthonormal vectors.


## r2 layout refinement

- On the projection card, the label $u_1=v_1$ is moved farther away from the vector so it no longer intercepts the arrow.
- On the final bridge card, the formula block is moved downward to clear the yellow text and create a more balanced composition.


## r3 card-1 goal box

- Card 1 adds a small boxed preview on the right that highlights the orthogonal vectors produced by the projection step.
- The box previews $u_1=v_1$, the projected-subtraction formula for $u_2$, and the orthogonality conclusion $u_1\cdot u_2=0$.


## r4 card-2 projection box

- The small explanatory box is moved from card 1 to card 2, matching the intended emphasis.
- Card 2 now highlights two geometric facts: the projection is parallel to $u_1$, and the leftover $v_2-\operatorname{proj}_{u_1}v_2$ is perpendicular to $u_1$.
- Card 1 returns to a simpler opening composition.


## r5 card-2 right-angle marker

- Card 2 removes the boxed formula callout.
- Instead, the diagram now uses a standard small right-angle marker at the projection point to indicate that the leftover direction is perpendicular to $u_1$.
- The emphasis is now geometric rather than boxed algebraic.


## r6 card-2 right-angle placement

- Card 2 moves the standard right-angle marker to the geometrically natural quadrant between the visible projection segment back toward the origin and the residual segment toward $v_2$.
- The marker now sits where the two displayed perpendicular segments actually meet, rather than on the opposite side of the projection point.
