# Checkpoint 210 — The Minimum Principle

This lesson returns to the positive-definite chapter after the SVD sequence and
develops the Rayleigh quotient as a minimization principle. It first recovers the
smallest eigenvalue, then excludes previously found eigen-directions to recover the
remaining eigenvalues one at a time.

## Numerical spine

- `A=[[2,1,0],[1,2,0],[0,0,4]]` is symmetric positive definite.
- Its ordered eigenvalues are `1`, `3`, and `4`.
- Orthonormal eigenvectors are
  `v1=(1,-1,0)/sqrt(2)`, `v2=(1,1,0)/sqrt(2)`, and `v3=(0,0,1)`.
- The Rayleigh quotient is `R_A(x)=(x^T A x)/(x^T x)` for `x != 0`.
- Writing `x=c1 v1+c2 v2+c3 v3` gives
  `R_A(x)=(c1^2+3c2^2+4c3^2)/(c1^2+c2^2+c3^2)`.
- Therefore `1 <= R_A(x) <= 4`.
- The unrestricted minimum is `lambda1=1` at `v1`.
- Constraining `x` perpendicular to `v1` gives `lambda2=3` at `v2`.
- Constraining `x` perpendicular to both `v1` and `v2` gives `lambda3=4`
  at `v3`.

## Story

1. Ask whether minimization can recover the eigenvalues of a symmetric matrix.
2. Define the Rayleigh quotient as quadratic energy divided by squared length.
3. Show that scaling a vector does not change the quotient.
4. Introduce the example's three orthonormal eigen-directions.
5. Expand an arbitrary vector in the eigenvector basis.
6. Interpret the quotient as a weighted average of `1`, `3`, and `4`.
7. Recover the first eigenvalue as the unrestricted minimum.
8. Pause and ask what happens when the lowest-energy direction is excluded.
9. Add successive orthogonality constraints to recover the second and third
   eigenvalues.
10. State the general successive minimum principle.

## Scope boundary

The lesson does not introduce finite elements, Ritz approximation, Galerkin
methods, generalized eigenvalue problems, or numerical optimization algorithms.

## Files

```text
engine/minimum_principle.py
scenes/minimum_principle_presentation.py
tests/test_minimum_principle.py
tests/test_minimum_principle_presentation.py
scripts/check_cp210_minimum_principle.zsh
scripts/render_cp210_minimum_principle.zsh
CHECKPOINT_210.md
apply_checkpoint_210.zsh
```

## Environment

Checkpoint 210 assumes Python 3.12 and Manim Community 0.21.0. Both scripts set
the repository root on `PYTHONPATH` before checking or rendering.

```zsh
conda activate seeingla-manim021
scripts/check_cp210_minimum_principle.zsh
scripts/render_cp210_minimum_principle.zsh
```

The render script intentionally produces only a low-quality preview.
