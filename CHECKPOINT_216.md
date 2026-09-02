# Checkpoint 216 — Full SVD and the Four Fundamental Subspaces

This lesson answers CP215's question about missing directions by showing how the
full SVD organizes both the input and output spaces. The columns of `V` split the
domain into the row space and null space. The columns of `U` split the codomain
into the column space and left null space.

## Numerical spine

Use the rank-one rectangular matrix

```text
A=[[1,1],
   [1,1],
   [0,0]].
```

- `A:R^2 -> R^3`, with `m=3`, `n=2`, and `r=1`.
- Singular values are `2` and `0`.
- `v_1=(1,1)/sqrt(2)` spans the row space and maps to `2u_1`.
- `v_2=(1,-1)/sqrt(2)` spans the null space and maps to zero.
- `u_1=(1,1,0)/sqrt(2)` spans the column space.
- `u_2=(1,-1,0)/sqrt(2)` and `u_3=(0,0,1)` span the left null space.
- The full factors have dimensions `U:3x3`, `Sigma:3x2`, and `V^T:2x2`.

## Story

1. Present the rectangular rank-one map and its input/output dimensions.
2. Show the full `V^T -> Sigma -> U` pipeline.
3. Contrast the surviving input direction `v_1` with the lost direction `v_2`.
4. Pause and ask which fundamental subspace contains each direction.
5. Use `V` to split `R^2` into the row space and null space.
6. Use `U` to split `R^3` into the column space and left null space.
7. Show the active and zero singular-value lanes.
8. Display the complete rectangular factors structurally.
9. Derive the four subspace dimensions from `m`, `n`, and `r`.
10. Finish with the SVD as orthonormal bases for all four subspaces.

## Architecture

`SVDFundamentalSubspaces` composes the established `RankCollapse` engine and
adds deterministic orthonormal completions for the full `U` and `V` bases. It
supports domain and codomain orthogonal decompositions without depending on
Manim. The scene remains a presentation adapter.

## Scope boundary

This checkpoint does not introduce the pseudoinverse, least-squares or
minimum-norm formulas, condition numbers, Eckart–Young approximation, image
compression, or PCA.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp216_svd_fundamental_subspaces.zsh
scripts/render_cp216_svd_fundamental_subspaces.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/svd_fundamental_subspaces.py
scenes/svd_fundamental_subspaces_presentation.py
tests/test_svd_fundamental_subspaces.py
tests/test_svd_fundamental_subspaces_presentation.py
scripts/check_cp216_svd_fundamental_subspaces.zsh
scripts/render_cp216_svd_fundamental_subspaces.zsh
CHECKPOINT_216.md
apply_checkpoint_216.zsh
```
