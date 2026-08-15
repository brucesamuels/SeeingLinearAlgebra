# Checkpoint 159 - Gram-Schmidt in R^3

## Purpose

Extend Gram-Schmidt from the two-vector mechanism to the first fully three-dimensional case.
This checkpoint is the conceptual payoff: the third vector must lose **two earlier projection
components**, not just one.

The lesson is designed so it can be placed flexibly in the chapter sequence. It follows
naturally after projection, orthogonal sets, or the two-vector Gram-Schmidt example.

## Mathematical narrative

1. Start with three independent vectors in `R^3`.
2. Re-establish the first two orthogonal directions:
   `u_1 = v_1` and `u_2 = v_2 - proj_{u_1} v_2`.
3. Begin with `v_3` and remove its `u_1` component.
4. Remove the remaining `u_2` component.
5. Reveal the orthogonal frame `u_1, u_2, u_3`.
6. State the general Gram-Schmidt pattern.
7. Note that normalization can be applied afterward if an orthonormal basis is desired.

The example is intentionally arithmetic-friendly:

\[
\mathbf v_1=(2,2,0),\qquad
\mathbf v_2=(2,0,2),\qquad
\mathbf v_3=(3,-1,1).
\]

Then

\[
\mathbf u_1=(2,2,0),
\qquad
\operatorname{proj}_{\mathbf u_1}\mathbf v_2=(1,1,0),
\qquad
\mathbf u_2=(1,-1,2).
\]

For the third vector,

\[
\operatorname{proj}_{\mathbf u_1}\mathbf v_3=(1,1,0),
\qquad
\mathbf w_3=(2,-2,1),
\]

and then

\[
\operatorname{proj}_{\mathbf u_2}\mathbf v_3=(1,-1,2),
\qquad
\mathbf u_3=(1,-1,-1).
\]

Finally,

\[
\mathbf u_1\cdot\mathbf u_2=0,
\qquad
\mathbf u_1\cdot\mathbf u_3=0,
\qquad
\mathbf u_2\cdot\mathbf u_3=0.
\]

## Files

- `engine/gram_schmidt_three_vectors.py`
- `scenes/gram_schmidt_three_vectors_presentation.py`
- `tests/test_gram_schmidt_three_vectors.py`
- `tests/test_gram_schmidt_three_vectors_presentation.py`
- `scripts/check_cp159_gram_schmidt_three_vectors.zsh`
- `scripts/render_cp159_gram_schmidt_three_vectors.zsh`
- `CHECKPOINT_159.md`

## Install

macOS Safari auto-unzips the download, so install from the extracted folder:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp159/apply_checkpoint_159.zsh
```

## Check

```zsh
zsh scripts/check_cp159_gram_schmidt_three_vectors.zsh
```

## Preview render

```zsh
zsh scripts/render_cp159_gram_schmidt_three_vectors.zsh -pql
```

The preview file is named:

```text
CP159_initial_three_vector_orthogonalization_preview.mp4
```

Do not commit until the preview has been visually approved.

## Visual review notes

- The 3D construction should begin comfortably inside the frame and stay inside the frame during the
  modest camera move on the orthogonal-frame card.
- Labels should stay readable and should travel with the geometry using fixed-orientation 3D labels.
- The third-vector cards should make the two-stage subtraction visually obvious: first remove the
  `u_1` component, then remove the `u_2` component.
- The final card should feel like a reusable recipe, not just the conclusion of a special example.


## r2 layout refinement

- Fixed-frame and fixed-orientation text is now registered with zero opacity first, so text no longer appears on screen before its intended animation begins.
- On cards 1 through 5, the 3D construction is larger and positioned lower so the geometry has more visual dominance.
- The camera zoom is increased to support the larger geometry while preserving the established card sequence.


## r3 runtime-safe fixed text

- Removes the recursive fixed-orientation helper that caused the r2 RecursionError.
- Fixed-frame text and fixed-orientation 3D labels are registered only immediately before their reveal animations, preventing pre-roll text without opacity hacks.
- Removes fixed registrations after each card to avoid stale hidden objects accumulating.
- Replaces the 0.01-second camera reset with an instantaneous camera orientation reset, eliminating the low-frame-rate warning.
- Preserves the larger, lower 3D composition introduced in r2.


## r4 composition refinement

- Cards 1-5 lower the shared 3D construction further so the vertex sits below the horizontal midpoint and the geometry carries more of the screen.
- Card 5 now rotates the orthogonal frame about the z-axis, rather than using a camera orbit, so the system itself turns around a clearer center of rotation.


## r5 composition refinement

- On cards 1-5, the 3D construction is pushed further down and enlarged again so it has stronger visual dominance.
- The figure labels are moved farther away from the vectors to reduce crowding and improve readability.


## r6 card-5 pairwise orthogonality views

- Card 5 no longer uses a generic system spin.
- Instead, it steps through three purposeful viewing directions: nearly along $u_3$, then nearly along $u_2$, then nearly along $u_1$.
- At each view, one pairwise orthogonality statement is revealed, so the rotation now directly supports the mathematics.
