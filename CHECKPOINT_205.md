# Checkpoint 205 — Why A-Transpose A Is Positive Semidefinite

This lesson continues the squared-norm idea from Cholesky and applies it to every
rectangular matrix. It introduces positive semidefiniteness, explains exactly when
zero Gram energy occurs, and connects positive definiteness to column independence.

## Numerical spine

- `A=[[1,0],[1,1],[0,1]]` has independent columns.
- `A^T A=[[2,1],[1,2]]`, reconnecting to the matrix from CP199.
- `x^T A^T A x=||Ax||^2>=0`.
- `B=[[1,2],[1,2],[0,0]]` has dependent columns.
- For `x=(-2,1)`, `Bx=0`, so `x^T B^T B x=0` although `x` is nonzero.

## Story

1. Recall Cholesky's squared-norm interpretation and ask whether the same pattern
   exists for an arbitrary rectangular matrix.
2. Form `A^T A` structurally and reconnect to the opening positive-definite matrix.
3. Derive the Gram-energy identity and define positive semidefiniteness.
4. Explain why negative Gram energy is impossible.
5. Use the independent columns of `A` to show why its Gram matrix is positive definite.
6. Pause and ask when a nonzero vector can still have zero Gram energy.
7. Use the dependent columns of `B` and the explicit null vector `(-2,1)` to produce
   zero energy.
8. Finish with the universal semidefinite result and the column-independence criterion.

Normal-equation solving and covariance applications remain outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp205_gram_matrix_definiteness.zsh
zsh scripts/render_cp205_gram_matrix_definiteness.zsh
```

The render command produces only a low-quality preview.
