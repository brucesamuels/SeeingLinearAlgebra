# Checkpoint 99 — Matrix–Matrix Multiplication

## Chapter role

CP99 follows the row–column rule and extends it from a matrix times a vector
to a matrix times another matrix.

Each entry of \(AB\) is produced by one row of \(A\) dotted with one column of
\(B\).

## Storyboard

1. Establish the compatibility rule:
   \[
   A_{m\times n}B_{n\times p}=C_{m\times p}.
   \]
2. Explain inner and outer dimensions.
3. Compute the upper-left entry.
4. Compute the remaining three entries.
5. State the general rule:
   \[
   c_{ij}=\sum_{k=1}^{n}a_{ik}b_{kj}.
   \]
6. Emphasize that matrix multiplication is not entrywise.
7. Show an incompatible product.
8. Contrast multiplication compatibility with matrix addition.
9. Include a Pause-and-Predict example.
10. Bridge to matrix multiplication as composition.

## Example

\[
A=
\begin{bmatrix}
1&2&-1\\
3&0&4
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
2&1\\
-1&3\\
5&2
\end{bmatrix}.
\]

Then

\[
AB=
\begin{bmatrix}
-5&5\\
26&11
\end{bmatrix}.
\]

## Files

- `engine/matrix_matrix_multiplication.py`
- `scenes/matrix_matrix_multiplication_presentation.py`
- `tests/test_matrix_matrix_multiplication.py`
- `tests/test_matrix_matrix_multiplication_presentation.py`
- `scripts/check_cp99_matrix_matrix_multiplication.zsh`
- `scripts/render_cp99_matrix_matrix_multiplication.zsh`
- `apply_checkpoint_99.zsh`

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp99/apply_checkpoint_99.zsh
~/Downloads/seeing_linear_algebra_cp99/apply_checkpoint_99.zsh
```

## Check

```zsh
./scripts/check_cp99_matrix_matrix_multiplication.zsh
```

## Render

```zsh
./scripts/render_cp99_matrix_matrix_multiplication.zsh
```

Do not commit until the render has been reviewed and approved.
