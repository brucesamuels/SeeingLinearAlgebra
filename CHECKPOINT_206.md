# Checkpoint 206 — Why Least Squares Has a Unique Solution

This lesson applies CP205's Gram-matrix result to least squares. It explains why
full column rank makes the normal equations uniquely solvable and why dependent
columns can produce different coefficient vectors with the same fitted vector.

## Numerical spine

- `A=[[1,0],[1,1],[0,1]]` and `b=(2,1,2)` continue the CP205 example.
- `A^T A=[[2,1],[1,2]]` and `A^T b=(3,3)`.
- The unique least-squares coefficient vector is `x_hat=(1,1)`.
- `A x_hat=(1,2,1)` and the residual is `(1,-1,1)`.
- `A^T r=0`, verifying residual orthogonality.
- `B=[[1,2],[1,2],[0,0]]` has dependent columns.
- `x_1=(3,0)` and `x_2=(1,1)` both give `B x=(3,3,0)`.
- Their difference `(-2,1)` lies in `null(B)`.

## Story

1. Recall the CP205 equivalence between independent columns and a
   positive-definite Gram matrix.
2. Present the least-squares objective and recall how residual orthogonality gives
   the normal equations.
3. Form the two-by-two normal equations structurally.
4. Pause and ask why the coefficient system must have exactly one solution.
5. Connect independent columns, positive definiteness, and invertibility.
6. Solve for `x_hat=(1,1)` and verify the residual orthogonality condition.
7. Contrast dependent columns using two distinct coefficient vectors with the same
   fitted vector.
8. Explain the entire coefficient family `x+t z` when `z` lies in the null space.
9. Finish with the full-column-rank uniqueness guarantee.

Covariance, pseudoinverses, conditioning, optimization algorithms, and a detailed
QR comparison remain outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp206_least_squares_uniqueness.zsh
zsh scripts/render_cp206_least_squares_uniqueness.zsh
```

The render command produces only a low-quality preview.
