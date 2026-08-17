# CP164 - Projection Matrices: Symmetric and Idempotent

## Purpose

CP164 returns to projection after the orthogonal-matrix lessons and makes the algebraic structure of a projection matrix explicit.

The central idea is that if the columns of `Q` form an orthonormal basis for a subspace `W`, then

\[
P=QQ^T
\]

is the orthogonal projection onto `W`.

The lesson then develops the two algebraic signatures of an orthogonal projection matrix:

\[
P^2=P,
\qquad
P^T=P.
\]

It closes by contrasting a projection matrix with an orthogonal matrix, so students do not confuse "orthogonal projection" with "orthogonal transformation."

## Concrete example

Use

\[
q=\frac1{\sqrt5}\begin{bmatrix}1\\2\end{bmatrix},
\qquad
P=qq^T
=\frac15
\begin{bmatrix}
1&2\\
2&4
\end{bmatrix}.
\]

For

\[
v=\begin{bmatrix}4\\1\end{bmatrix},
\]

we obtain

\[
Pv=\begin{bmatrix}6/5\\12/5\end{bmatrix},
\qquad
r=v-Pv=\begin{bmatrix}14/5\\-7/5\end{bmatrix}.
\]

The residual is perpendicular to the line spanned by `(1,2)`.

## Eight-card structure

1. **From orthonormal basis to projection matrix:** `P=QQ^T`.
2. **Algebra bridge from a general basis:** start with `P=A(A^TA)^{-1}A^T`; for orthonormal columns, `Q^TQ=I`, so `P=QQ^T`.
3. **Geometry of projection:** `v=Pv+r`, with a visible right-angle marker.
4. **Idempotence:** project once, then project again; the second projection does nothing.
5. **Symmetry:** derive `P^T=P` from `P=QQ^T`.
6. **Concrete numerical example:** build and apply `P`.
7. **Subspace versus orthogonal complement:** `Pq=q` and `Pn=0`.
8. **Projection matrix versus orthogonal matrix:** compare `P^2=P` with `Q^TQ=I`.

## Visual structure

Graphical cards reserve:

- a left geometry zone,
- a right mathematics zone,
- and a separate bottom explanatory band.

All coordinate graphics use the emphasized chapter grid style.

## Files

- `engine/projection_matrices.py`
- `scenes/projection_matrices_presentation.py`
- `tests/test_projection_matrices.py`
- `tests/test_projection_matrices_presentation.py`
- `scripts/check_cp164_projection_matrices.zsh`
- `scripts/render_cp164_projection_matrices.zsh`
- `CHECKPOINT_164.md`
- `apply_checkpoint_164.zsh`

## Review focus

Please check the low-quality preview for:

- clarity of the right-angle marker on the projection geometry card,
- whether the "project twice" animation makes `P^2=P` immediately intuitive,
- balance of the symmetry card,
- legibility of the concrete `2 x 2` example,
- and whether the final projection-versus-orthogonal comparison clearly separates the two ideas.


## r2 refinement

- Added a dedicated algebra card showing how the general full-column-rank projection formula `P=A(A^TA)^{-1}A^T` becomes `P=QQ^T` when the basis columns are orthonormal.
- On the final card, positioned "Projection matrix versus orthogonal matrix" at the midpoint of the actual open gap between the lesson title and the two box labels for better symmetry.
