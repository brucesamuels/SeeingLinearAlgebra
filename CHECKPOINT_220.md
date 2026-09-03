# Checkpoint 220 — Truncated SVD and the Best Low-Rank Approximation

This lesson turns the ordered SVD into a controlled approximation method. It
interprets a matrix as a sum of rank-one layers, discards the weakest layer,
measures the error, and states the Eckart–Young optimality theorem.

## Numerical spine

Use

```text
A=diag(5, 2, 1/2).
```

- The ordered singular values are `5`, `2`, and `1/2`.
- `A=5u_1v_1^T+2u_2v_2^T+(1/2)u_3v_3^T`.
- The rank-two truncation is `A_2=diag(5,2,0)`.
- The residual is `(1/2)u_3v_3^T`.
- Both the spectral and Frobenius errors are `1/2` because one layer is omitted.
- Keeping singular values `5` and `1/2` instead would give spectral error `2`.
- The approximation ladder has spectral errors `2`, `1/2`, and `0` at ranks
  one, two, and three.

## Story

1. Present the ordered singular values and ask whether a simpler matrix can preserve the main action.
2. Write the SVD as an ordered sum of rank-one layers.
3. Visualize the three layers according to their singular-value strengths.
4. Truncate after the first two layers.
5. Identify the residual as the discarded weakest layer.
6. Measure the residual in spectral and Frobenius norms.
7. State the Eckart–Young theorem for both norms.
8. Compare truncation with discarding a stronger component.
9. Build a rank-versus-error approximation ladder.
10. Finish with the truncated-SVD formula and its optimality meaning.

## Architecture

`TruncatedSVDApproximation` supplies ordered singular values, rank-one
components, truncations, residuals, spectral and Frobenius errors, and arbitrary
component selections. It supports rectangular matrices and has no Manim
dependency.

## Scope boundary

This checkpoint establishes the approximation theorem but does not yet apply it
to image compression, storage counts, retained energy, or PCA.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp220_truncated_svd_approximation.zsh
scripts/render_cp220_truncated_svd_approximation.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/truncated_svd_approximation.py
scenes/truncated_svd_approximation_presentation.py
tests/test_truncated_svd_approximation.py
tests/test_truncated_svd_approximation_presentation.py
scripts/check_cp220_truncated_svd_approximation.zsh
scripts/render_cp220_truncated_svd_approximation.zsh
CHECKPOINT_220.md
apply_checkpoint_220.zsh
```
