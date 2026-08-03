# Checkpoint 98 — The Row–Column Rule

## Chapter role

CP98 follows:

1. CP96 — Matrix Addition and Subtraction
2. CP97 — Scalar Multiplication of Matrices
3. CP94 — Matrix–Vector Multiplication as a Column Combination

CP98 now presents the same matrix–vector product from the row viewpoint:
each row of \(A\) computes one entry of \(A\mathbf{x}\).

## Storyboard

1. Revisit \(A\mathbf{x}\) as a column combination.
2. Reframe the same result as row-dot-vector computations.
3. Highlight the first row and compute the first output entry.
4. Highlight the second row and compute the second output entry.
5. State the general rule:
   \[
   (A\mathbf{x})_i=\sum_{j=1}^n a_{ij}x_j.
   \]
6. Explain the dimension condition.
7. Show an incompatible example.
8. Include a Pause-and-Predict calculation.
9. Reflect that rows compute entries while columns build the vector.
10. Bridge to matrix–matrix multiplication.

## Example

\[
A=
\begin{bmatrix}
2&-1&3\\
1&4&-2
\end{bmatrix},
\qquad
\mathbf{x}=
\begin{bmatrix}
3\\2\\-1
\end{bmatrix}.
\]

Then

\[
A\mathbf{x}
=
\begin{bmatrix}
(2)(3)+(-1)(2)+(3)(-1)\\
(1)(3)+(4)(2)+(-2)(-1)
\end{bmatrix}
=
\begin{bmatrix}
1\\13
\end{bmatrix}.
\]

## Files

- `engine/row_column_rule.py`
- `scenes/row_column_rule_presentation.py`
- `tests/test_row_column_rule.py`
- `tests/test_row_column_rule_presentation.py`
- `scripts/check_cp98_row_column_rule.zsh`
- `scripts/render_cp98_row_column_rule.zsh`
- `apply_checkpoint_98.zsh`

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp98/apply_checkpoint_98.zsh
~/Downloads/seeing_linear_algebra_cp98/apply_checkpoint_98.zsh
```

## Check

```zsh
./scripts/check_cp98_row_column_rule.zsh
```

## Render

```zsh
./scripts/render_cp98_row_column_rule.zsh
```

Do not commit until the render has been reviewed and approved.
