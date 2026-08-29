# Checkpoint 204 — Cholesky: A Matrix Square Root

This lesson absorbs the positive diagonal factor from CP203 into the triangular
factors. The result is the unique positive-diagonal Cholesky factor and a direct
squared-norm interpretation of positive quadratic energy.

## Numerical spine

- `A=[[4,2,0],[2,3,1],[0,1,2]]`
- `D=diag(4,2,3/2)` and `D^(1/2)=diag(2,sqrt(2),sqrt(3/2))`.
- `R=D^(1/2)L^T`.
- `R=[[2,1,0],[0,sqrt(2),1/sqrt(2)],[0,0,sqrt(3/2)]]`.
- `A=R^T R`.
- `x^T A x=||Rx||^2`.

## Story

1. Recall `A=LDL^T` and ask what positive diagonal entries allow.
2. Take the positive square root of every diagonal pivot.
3. Absorb `D^(1/2)` into the triangular factors and define `R`.
4. Structurally assemble and verify `A=R^T R`.
5. Build the upper-triangular entries in Cholesky algorithm order.
6. Rewrite the quadratic energy as the squared norm `||Rx||^2`.
7. Pause and ask what would prevent the next positive square root from existing.
8. Connect failure to a nonpositive Cholesky pivot.
9. Finish with existence and uniqueness for symmetric positive definite matrices.

Applications to systems, least squares, and covariance remain outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp204_positive_definite_cholesky.zsh
zsh scripts/render_cp204_positive_definite_cholesky.zsh
```

The render command produces only a low-quality preview.
