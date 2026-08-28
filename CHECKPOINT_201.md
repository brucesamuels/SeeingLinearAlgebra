# Checkpoint 201 — The Eigenvalue Test

This lesson explains why the extreme unit-direction energies from the first positive
definiteness lesson are eigenvalues, then turns that observation into the first
practical test for a symmetric matrix.

## Numerical spine

- `A=[[2,1],[1,2]]`
- `u+=(1,1)/sqrt(2)` has eigenvalue and unit energy `3`.
- `u-=(1,-1)/sqrt(2)` has eigenvalue and unit energy `1`.
- For unit vectors, `1 <= x^T A x <= 3`.
- In the eigenvector basis, `x^T A x=3c+^2+c-^2`.
- Generally, `x^T A x=sum(lambda_i c_i^2)` for a symmetric matrix.

## Story

1. Sweep a unit vector and ask which directions give the smallest and largest
   quadratic energies.
2. Stop on the two diagonal directions and reveal the values `3` and `1`.
3. Show structurally that these directions are eigenvectors.
4. Derive that a unit eigenvector's quadratic energy equals its eigenvalue.
5. Expand an arbitrary vector in the eigenvector basis and separate the energy into
   eigenvalue-weighted squares.
6. Connect positive, zero, and negative coefficient signs to the three geometries
   shown in Checkpoint 200.
7. Finish with the symmetric-matrix eigenvalue test for positive definiteness.

Elimination criteria, determinant criteria, and matrix factorizations remain outside
this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp201_positive_definite_eigenvalue_test.zsh
zsh scripts/render_cp201_positive_definite_eigenvalue_test.zsh
```

The render command produces only a low-quality preview.
