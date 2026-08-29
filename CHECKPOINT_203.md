# Checkpoint 203 — The LDL-Transpose Factorization

This lesson turns CP202's elimination data into a matrix factorization. The
elimination multipliers form a unit lower-triangular matrix, the pivots form a
diagonal matrix, and the factorization becomes the matrix form of completing squares.

## Numerical spine

- `A=[[4,2,0],[2,3,1],[0,1,2]]`
- Elimination multipliers are `l21=1/2`, `l31=0`, and `l32=1/2`.
- Elimination pivots are `4`, `2`, and `3/2`.
- `L=[[1,0,0],[1/2,1,0],[0,1/2,1]]`.
- `D=diag(4,2,3/2)`.
- `A=LDL^T`.
- With `y=L^T x`, the energy is `x^T A x=y^T D y`.

## Story

1. Recall CP202's pivots and ask where the elimination multipliers went.
2. Follow the shrinking symmetric active block and record each pivot and multiplier.
3. Place the multipliers below the diagonal of `L` and the pivots on the diagonal of
   `D`.
4. Structurally assemble and verify `A=LDL^T`.
5. Change coordinates with `y=L^T x` and rewrite the quadratic energy as `y^T D y`.
6. Reveal the corresponding three-square expression.
7. Pause and ask which factor controls the sign of the energy.
8. Finish with the positive-diagonal test for a symmetric `LDL^T` factorization.

The next square-root-based factorization remains outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp203_positive_definite_ldlt.zsh
zsh scripts/render_cp203_positive_definite_ldlt.zsh
```

The render command produces only a low-quality preview.
