# Checkpoint 158 - From Orthogonal to Orthonormal

## Purpose

Continue directly from CP157. Gram-Schmidt produced the orthogonal pair

\[
\mathbf u_1=(1,2),\qquad \mathbf u_2=(2,-1).
\]

CP158 shows that normalization changes only vector length, not direction. Dividing
each orthogonal vector by its magnitude produces the orthonormal pair

\[
\mathbf e_1=\frac{1}{\sqrt5}(1,2),\qquad
\mathbf e_2=\frac{1}{\sqrt5}(2,-1).
\]

The geometry emphasizes that the vectors remain perpendicular while their tips move
to the unit circle.

## Mathematical narrative

1. Recall the orthogonal pair from CP157 and note that both vectors have length `sqrt(5)`.
2. Normalize `u_1` to create `e_1`; the arrow shrinks along its existing direction.
3. Normalize `u_2` to create `e_2` in the same way.
4. Place `e_1` and `e_2` on the unit circle and retain the right-angle marker.
5. Summarize what normalization preserves: direction, orthogonality, and span.
6. Bridge to QR by arranging the orthonormal vectors as the columns of `Q`, with `Q^T Q = I`.

## Files

- `engine/orthonormalization.py`
- `scenes/orthonormalization_presentation.py`
- `tests/test_orthonormalization.py`
- `tests/test_orthonormalization_presentation.py`
- `scripts/check_cp158_orthonormalization.zsh`
- `scripts/render_cp158_orthonormalization.zsh`
- `CHECKPOINT_158.md`

## Install

macOS Safari auto-unzips the download, so install from the extracted folder:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp158/apply_checkpoint_158.zsh
```

## Check

```zsh
zsh scripts/check_cp158_orthonormalization.zsh
```

## Preview render

```zsh
zsh scripts/render_cp158_orthonormalization.zsh -pql
```

Preview file:

```text
CP158_initial_orthonormalization_preview.mp4
```

Do not commit until the preview has been visually approved.

## Visual review notes

- Keep the same orange/purple vector identity established in CP157.
- The normalization animations should visibly shorten the arrows along the same rays; there should be no apparent rotation.
- The unit-circle card should make both unit length and perpendicularity immediately visible.
- The small right-angle marker should remain attached to the diagram and should not compete with labels.
- The summary card should remain spacious and avoid a surrounding formula box.
- The final QR bridge is intentionally brief; the factorization itself belongs to the next lesson.


## r2 grid refinement

- Cards 1 and 2 now use a more visible coordinate grid behind the vector diagrams.
- Later cards keep their existing grid treatment so the stronger grid is reserved for the opening normalization setup.


## r3 grid on all graphic cards

- The same emphasized coordinate grid is now used on every graphical card, not just the first two.
- The normalization cards and the unit-circle card now share a consistent visual grid treatment.
