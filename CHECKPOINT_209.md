# Checkpoint 209 — Computing the SVD from A-Transpose A

This lesson turns CP208's geometric SVD interpretation into a reusable computation.
It forms a Gram matrix, computes ordered eigenpairs, takes square roots, recovers
left singular vectors without a second eigenproblem, assembles the thin factors,
and verifies the reconstruction.

## Numerical spine

- `B=[[1,1],[1,-1],[1,1]]` is a three-by-two full-column-rank matrix.
- `B^T B=[[3,1],[1,3]]`.
- The Gram eigenvalues are `4` and `2`.
- Right singular vectors are `(1,1)/sqrt(2)` and `(1,-1)/sqrt(2)`.
- Singular values are `2` and `sqrt(2)`.
- `u_1=(1,0,1)/sqrt(2)` and `u_2=(0,1,0)`.
- The thin dimensions are `U:3x2`, `Sigma:2x2`, and `V^T:2x2`.
- The product `U Sigma V^T` reconstructs `B` exactly.

## Story

1. Present the new rectangular matrix and the factorization goal.
2. Form `B^T B` structurally.
3. Solve the characteristic equation for its two eigenvalues.
4. Normalize the right singular vectors.
5. Take nonnegative square roots to obtain the singular values.
6. Pause and ask how to recover `U` without another eigenvalue problem.
7. Use `u_i=Bv_i/sigma_i` for both mapped directions.
8. Assemble the dimensioned thin SVD with compact structural matrices.
9. Verify that the factors reconstruct every entry of `B`.
10. Explain paired sign ambiguity in `u_i` and `v_i`.
11. Finish with the reusable five-step recipe.

Zero singular values, extra left-singular directions, rank and null spaces,
pseudoinverses, least-squares formulas, and low-rank approximation remain outside
this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp209_svd_computation.zsh
zsh scripts/render_cp209_svd_computation.zsh
```

The render command produces only a low-quality preview.
