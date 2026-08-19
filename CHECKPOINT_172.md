# Checkpoint 172 — Computing Eigenvalues in a 3×3 Example

## Purpose

Checkpoint 172 extends the characteristic-equation method from CP171 into a fully worked `3 x 3` example. The lesson emphasizes that the method is unchanged, while determinant structure becomes more important.

## Example

The lesson uses

\[
A=\begin{bmatrix}
4&1&0\\
2&3&0\\
0&0&1
\end{bmatrix}.
\]

Then

\[
A-\lambda I=
\begin{bmatrix}
4-\lambda&1&0\\
2&3-\lambda&0\\
0&0&1-\lambda
\end{bmatrix}.
\]

The third column has two zeros, so cofactor expansion gives

\[
\det(A-\lambda I)
=(1-\lambda)
\begin{vmatrix}
4-\lambda&1\\
2&3-\lambda
\end{vmatrix}.
\]

The remaining `2 x 2` determinant is computed with `ad-bc`:

\[
(1-\lambda)\big((4-\lambda)(3-\lambda)-2\big)=0.
\]

This simplifies to

\[
(1-\lambda)(\lambda^2-7\lambda+10)=0
\]

and factors as

\[
(1-\lambda)(\lambda-5)(\lambda-2)=0.
\]

Thus

\[
\lambda=1,\qquad \lambda=2,\qquad \lambda=5.
\]

## Scene sequence

1. Present the `3 x 3` matrix and explain that the zero structure will help.
2. Build `A - lambda I`, subtracting lambda from all three diagonal entries.
3. Display the full `3 x 3` determinant equation.
4. Expand along the third column, where two entries are zero.
5. Reduce to a `2 x 2` determinant and animate the `ad-bc` computation.
6. Simplify the quadratic factor.
7. Factor and read off all three eigenvalues.
8. End with a reusable `3 x 3` workflow emphasizing strategic determinant computation.

## Visual constraints

- Fixed 2D camera.
- Explicit vertical bands for banner, title, heading, mathematics, and supporting text.
- Full `3 x 3` determinant is shown before any reduction.
- Cofactor expansion is motivated by visible zeros rather than skipped.
- The remaining `2 x 2` determinant is worked explicitly.
- No trace/determinant shortcut replaces the characteristic-equation computation.

## Files

- `engine/computing_eigenvalues.py`
- `scenes/computing_eigenvalues_presentation.py`
- `tests/test_computing_eigenvalues.py`
- `tests/test_computing_eigenvalues_presentation.py`
- `scripts/check_cp172_computing_eigenvalues.zsh`
- `scripts/render_cp172_computing_eigenvalues.zsh`
- `CHECKPOINT_172.md`

## Development workflow

Run:

```zsh
zsh scripts/check_cp172_computing_eigenvalues.zsh
```

Then preview:

```zsh
zsh scripts/render_cp172_computing_eigenvalues.zsh
```

Do not commit until the rendered lesson is visually approved.
