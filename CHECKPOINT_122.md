# Checkpoint 122: Inverse by Gauss-Jordan Elimination

## Purpose

Interpret matrix inversion as the multiple-right-hand-side problem

\[
AX=I,
\]

and apply Gauss-Jordan row operations to

\[
[A\mid I]\longrightarrow[I\mid A^{-1}].
\]

## Mathematical example

\[
A=\begin{bmatrix}
1&2&1\\
0&1&3\\
0&0&2
\end{bmatrix}.
\]

Apply the four row operations

\[
R_3\leftarrow \frac12R_3,
\]

\[
R_2\leftarrow R_2-3R_3,
\]

\[
R_1\leftarrow R_1-R_3,
\]

\[
R_1\leftarrow R_1-2R_2.
\]

The completed block is

\[
\left[
\begin{array}{ccc|ccc}
1&0&0&1&-2&\frac52\\
0&1&0&0&1&-\frac32\\
0&0&1&0&0&\frac12
\end{array}
\right],
\]

so

\[
A^{-1}=\begin{bmatrix}
1&-2&\frac52\\
0&1&-\frac32\\
0&0&\frac12
\end{bmatrix}.
\]

## Multiple-right-hand-side interpretation

Writing

\[
X=\begin{bmatrix}\mathbf x_1&\mathbf x_2&\mathbf x_3\end{bmatrix},
\qquad
I=\begin{bmatrix}\mathbf e_1&\mathbf e_2&\mathbf e_3\end{bmatrix},
\]

shows that the columns of the inverse solve

\[
A\mathbf x_j=\mathbf e_j.
\]

## Elementary-matrix interpretation

If the four row operations correspond to elementary matrices
\(E_1,E_2,E_3,E_4\), then

\[
E_4E_3E_2E_1[A\mid I]
=
[I\mid E_4E_3E_2E_1].
\]

Therefore

\[
A^{-1}=E_4E_3E_2E_1.
\]

## Files

- `engine/gauss_jordan_inverse.py`
- `scenes/gauss_jordan_inverse_presentation.py`
- `tests/test_gauss_jordan_inverse.py`
- `tests/test_gauss_jordan_inverse_presentation.py`
- `scripts/check_cp122_gauss_jordan_inverse.zsh`
- `scripts/render_cp122_gauss_jordan_inverse.zsh`

## Validation

```zsh
./scripts/check_cp122_gauss_jordan_inverse.zsh
```

Render:

```zsh
./scripts/render_cp122_gauss_jordan_inverse.zsh
```
