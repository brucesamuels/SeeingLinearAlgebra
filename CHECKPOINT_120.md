# Checkpoint 120 — Elimination as Matrix Multiplication

## Purpose

Checkpoint 120 continues the elementary-matrix work of CP119 by composing the
individual elimination matrices into a single operator and then reversing that
operator to obtain the LU factorization.

## Mathematical example

The lesson uses

\[
A=\begin{bmatrix}
2&1&1\\
4&-6&0\\
-2&7&2
\end{bmatrix}.
\]

The elimination multipliers are

\[
m_{21}=2,\qquad m_{31}=-1,\qquad m_{32}=-1.
\]

Three elementary matrices produce

\[
E_3E_2E_1A=U,
\qquad
U=\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&0&1
\end{bmatrix}.
\]

Their product is

\[
E=E_3E_2E_1=
\begin{bmatrix}
1&0&0\\
-2&1&0\\
-1&1&1
\end{bmatrix}.
\]

Reversing the product gives

\[
A=E_1^{-1}E_2^{-1}E_3^{-1}U=LU,
\]

where

\[
L=\begin{bmatrix}
1&0&0\\
2&1&0\\
-1&-1&1
\end{bmatrix}.
\]

## Presentation sequence

1. Bridge from the previously developed individual elementary matrices.
2. State the goal of reducing \(A\) to upper-triangular \(U\).
3. Animate all three elimination products.
4. Compose the elementary matrices in the correct order.
5. Multiply them into the combined elimination matrix \(E\).
6. Reverse the product to recover \(A\) from \(U\).
7. Multiply the inverse elementary matrices into \(L\).
8. Connect each elimination multiplier to entries of \(E\) and \(L\).
9. Verify \(LU=A\).
10. Summarize LU factorization as Gaussian elimination written as a matrix identity.

## Files

- `engine/elimination_matrix_multiplication.py`
- `scenes/elimination_matrix_multiplication_presentation.py`
- `tests/test_elimination_matrix_multiplication.py`
- `tests/test_elimination_matrix_multiplication_presentation.py`
- `scripts/check_cp120_elimination_matrix_multiplication.zsh`
- `scripts/render_cp120_elimination_matrix_multiplication.zsh`

## Local verification

```zsh
./scripts/check_cp120_elimination_matrix_multiplication.zsh
./scripts/render_cp120_elimination_matrix_multiplication.zsh
```
