# Checkpoint 208 — Why the Singular Value Decomposition?

This lesson begins the SVD sequence by deriving its geometric structure from the
positive-definite Gram matrix introduced in CP205. It explains singular values,
right and left singular vectors, orthogonal mapped directions, and the conceptual
meaning of `A=U Sigma V^T` without yet becoming an algorithm lesson.

## Numerical spine

- Reuse `A=[[1,0],[1,1],[0,1]]` from CP205–CP206.
- `A^T A=[[2,1],[1,2]]`.
- Its orthonormal eigenvectors are
  `v_1=(1,1)/sqrt(2)` and `v_2=(1,-1)/sqrt(2)`.
- The corresponding eigenvalues are `3` and `1`.
- Singular values are `sigma_1=sqrt(3)` and `sigma_2=1`.
- `A v_1=sqrt(3) u_1`, where `u_1=(1,2,1)/sqrt(6)`.
- `A v_2=u_2`, where `u_2=(1,0,-1)/sqrt(2)`.
- The thin factorization reconstructs the original three-by-two matrix.

## Story

1. Recall that `A^T A` stores directional information about rectangular `A`.
2. Find its orthonormal eigenvector directions and positive eigenvalues.
3. Pause and ask which stretch factors `A` assigns to those directions.
4. Define singular values as nonnegative square roots of Gram eigenvalues.
5. Normalize the mapped directions to obtain the left singular vectors.
6. Prove that distinct Gram eigenvectors map to orthogonal output directions.
7. Show a unit circle becoming an ellipse in singular-vector coordinates.
8. Separate the transformation into `V^T`, diagonal stretching by `Sigma`, and `U`.
9. Display the explicit structural factorization.
10. Finish with the general SVD pattern and the roles of all three factors.

Computational procedure, zero singular values, rank and null spaces, the
pseudoinverse, least-squares solution formulas, and low-rank approximation remain
for later checkpoints.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp208_svd_introduction.zsh
zsh scripts/render_cp208_svd_introduction.zsh
```

The render command produces only a low-quality preview.
