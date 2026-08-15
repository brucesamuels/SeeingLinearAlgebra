# Checkpoint 160 - QR Factorization: Gram-Schmidt in Matrix Form

## Purpose

Turn the geometry of Gram-Schmidt into the matrix factorization

\[
A=QR.
\]

The lesson deliberately reuses the two-dimensional vectors from the earlier Gram-Schmidt and
orthonormalization lessons so that QR appears as a repackaging of familiar geometry rather than a
new computational trick.

## Example

\[
A=\begin{bmatrix}1&4\\2&3\end{bmatrix},
\qquad
\mathbf a_1=(1,2),
\qquad
\mathbf a_2=(4,3).
\]

Gram-Schmidt and normalization give

\[
\mathbf q_1=\frac1{\sqrt5}(1,2),
\qquad
\mathbf q_2=\frac1{\sqrt5}(2,-1),
\]

so

\[
Q=\frac1{\sqrt5}
\begin{bmatrix}
1&2\\
2&-1
\end{bmatrix},
\qquad Q^TQ=I.
\]

The original columns have orthonormal coordinates

\[
\mathbf a_1=\sqrt5\,\mathbf q_1+0\,\mathbf q_2,
\]

and

\[
\mathbf a_2=2\sqrt5\,\mathbf q_1+\sqrt5\,\mathbf q_2.
\]

Those coordinate columns form

\[
R=
\begin{bmatrix}
\sqrt5&2\sqrt5\\
0&\sqrt5
\end{bmatrix},
\]

and therefore

\[
A=QR.
\]

## Six-card sequence

1. Begin with the columns of `A` on an emphasized coordinate grid.
2. Recall the orthonormal columns `q_1,q_2` and form `Q`.
3. Express `a_1` in the orthonormal basis; reveal the first column of `R`.
4. Express `a_2` with a head-to-tail geometric decomposition; reveal the second column of `R`.
5. Assemble `A`, `Q`, and upper-triangular `R`; reveal `A=QR`.
6. Use `Q^TQ=I` to convert `Ax=b` into the triangular solve `Rx=Q^Tb`, then pose the least-squares question.

## Install

Safari normally expands the ZIP automatically. From the repository root:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp160/apply_checkpoint_160.zsh
```

## Check

```zsh
zsh scripts/check_cp160_qr_factorization.zsh
```

## Preview

```zsh
zsh scripts/render_cp160_qr_factorization.zsh -pql
```

Preview filename:

```text
CP160_initial_qr_factorization_preview.mp4
```

Do not commit until the preview has been visually approved.


## r2 - computational shortcut for R

A dedicated card now derives `R` by multiplying the factorization by the inverse of `Q`:

\[
A=QR
\quad\Longrightarrow\quad
Q^{-1}A=Q^{-1}QR=R.
\]

For the square orthogonal matrix in this example,

\[
Q^{-1}=Q^T,
\]

so

\[
R=Q^TA.
\]

The card then carries out the numerical multiplication

\[
R=\frac1{\sqrt5}
\begin{bmatrix}1&2\\2&-1\end{bmatrix}
\begin{bmatrix}1&4\\2&3\end{bmatrix}
=\frac1{\sqrt5}
\begin{bmatrix}5&10\\0&5\end{bmatrix}
=\begin{bmatrix}\sqrt5&2\sqrt5\\0&\sqrt5\end{bmatrix}.
\]

This is presented as a computational shortcut after the geometric construction of `R`, not as a replacement for the Gram-Schmidt interpretation.


## r3 inverse-card title spacing

- On the computation card, the yellow explanatory titles are moved upward to clear the derivation and matrix multiplication more comfortably.
- All mathematical content and pacing are otherwise unchanged.


## r4 right-side title clearance

- On the computation card, the right-hand yellow title is moved higher and the right computation block is lowered slightly.
- This gives extra clearance above the first line of mathematics on the viewer-right side.
