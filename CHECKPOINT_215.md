# Checkpoint 215 — What Does a Zero Singular Value Mean?

This checkpoint opens **Singular Values, Rank, and Approximation** by showing
what a matrix loses when one singular value becomes zero. It continues the SVD
bridge established in CP208–CP209 without repeating their full-column-rank
derivation or computation lesson.

## Numerical spine

- `A=[[1,1],[1,1]]` has rank one.
- `A^T A=[[2,2],[2,2]]` has eigenvalues `4` and `0`.
- The singular values are `sigma_1=2` and `sigma_2=0`.
- `v_1=(1,1)/sqrt(2)` survives: `A v_1=2u_1`.
- `v_2=(1,-1)/sqrt(2)` is lost: `A v_2=0`.
- The unit circle maps to the segment from `-2u_1` to `2u_1`.
- `N(A)=span{v_2}` and `rank(A)=1`, the number of positive singular values.
- The reduced rank-one factorization is `A=2u_1v_1^T`.

## Story

1. Ask what changes when a matrix erases an input direction.
2. Animate sampled points on the unit circle into a line segment.
3. Contrast the surviving direction `v_1` with the lost nonzero direction `v_2`.
4. Pause and ask where the lost direction is recorded in the SVD.
5. Form `A^T A` and find eigenvalues `4` and `0`.
6. Take square roots to obtain singular values `2` and `0`.
7. Connect `sigma_2=0` to `Av_2=0` and the null space.
8. Count positive singular values to obtain the rank.
9. Show the reduced rank-one SVD and finish with the loss-of-direction meaning.

## Architecture

`ZeroSingularValueModel` is renderer-independent and composes the established
`RankCollapse` engine for singular values, rank, nullity, row space, image, and
kernel data. The Manim scene remains a thin presentation layer.

## Scope boundary

This checkpoint does not introduce full-versus-reduced SVD conventions,
pseudoinverses, least-squares or minimum-norm formulas, condition numbers,
Eckart–Young approximation, image compression, or PCA.

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp215_svd_zero_singular_value.zsh
scripts/render_cp215_svd_zero_singular_value.zsh
```

The render script produces only a low-quality preview.

## Files

```text
engine/svd_zero_singular_value.py
scenes/svd_zero_singular_value_presentation.py
tests/test_svd_zero_singular_value.py
tests/test_svd_zero_singular_value_presentation.py
scripts/check_cp215_svd_zero_singular_value.zsh
scripts/render_cp215_svd_zero_singular_value.zsh
CHECKPOINT_215.md
apply_checkpoint_215.zsh
```
