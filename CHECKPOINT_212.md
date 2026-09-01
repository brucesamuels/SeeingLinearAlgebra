# Checkpoint 212 — Positive Definiteness: The Big Picture

This lesson closes the positive-definite sequence by organizing its central ideas
into one coherent toolkit. It contrasts positive definite, positive semidefinite,
and indefinite energy; consolidates six equivalent positive-definiteness tests;
and shows how to choose a test based on the information already available.

## Numerical spine

- `A=[[2,1],[1,2]]` is positive definite.
- Its eigenvalues are `1` and `3`.
- Its elimination pivots are `2` and `3/2`.
- Its leading principal minors are `2` and `3`.
- Its `LDL^T` diagonal is `D=diag(2,3/2)`.
- It has an invertible Cholesky factor `A=R^T R`.
- `B=[[1,1],[1,1]]` is positive semidefinite and has zero energy in direction
  `(1,-1)`.
- `C=[[1,0],[0,-1]]` is indefinite: its energy is positive in direction `(1,0)`
  and negative in direction `(0,1)`.

## Equivalent tests for a real symmetric matrix

The following statements are presented as equivalent:

- `x^T A x>0` for every nonzero `x`.
- Every eigenvalue is positive.
- Every elimination pivot is positive without row exchanges.
- Every leading principal minor is positive.
- `A=LDL^T` with positive diagonal `D`.
- `A=R^T R` with invertible triangular `R`.

## Story

1. Present three symmetric matrices and pause for classification.
2. Distinguish positive definite, positive semidefinite, and indefinite energy.
3. Focus on `A=[[2,1],[1,2]]` as the common positive-definite example.
4. Connect the energy definition to the eigenvalue test.
5. Connect elimination pivots to leading principal minors.
6. Connect `LDL^T` and Cholesky to weighted squares and squared norms.
7. Assemble the six equivalent statements into one toolkit.
8. Give a practical decision map for geometry, spectral data, elimination, and
   solving.
9. Reconnect the energy idea to Gram matrices, covariance, SVD, and minimization.
10. Finish with `positive energy -> unique minimum -> unique solution`.

## Scope boundary

This is a synthesis lesson. It does not introduce new tests, numerical algorithms,
finite-element extensions, weak forms, convergence theory, or higher-dimensional
applications.

## Files

```text
engine/positive_definiteness_summary.py
scenes/positive_definiteness_summary_presentation.py
tests/test_positive_definiteness_summary.py
tests/test_positive_definiteness_summary_presentation.py
scripts/check_cp212_positive_definiteness_summary.zsh
scripts/render_cp212_positive_definiteness_summary.zsh
CHECKPOINT_212.md
apply_checkpoint_212.zsh
```

## Environment

Checkpoint 212 assumes Python 3.12 and Manim Community 0.21.0. Both scripts place
the repository root on `PYTHONPATH` before checking or rendering.

```zsh
conda activate seeingla-manim021
scripts/check_cp212_positive_definiteness_summary.zsh
scripts/render_cp212_positive_definiteness_summary.zsh
```

The render script intentionally produces only a low-quality preview.
