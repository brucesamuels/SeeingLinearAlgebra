# Checkpoint 219 — Small Singular Values and Conditioning

This lesson distinguishes invertibility from numerical stability. An invertible
map can strongly compress one direction, forcing its inverse to amplify errors
in that direction. The ratio of the largest to smallest singular value measures
the worst directional imbalance.

## Numerical spine

Use

```text
A=[[4,   0],
   [0, 1/4]].
```

- `A` is a bijection and has determinant `1`.
- Its singular values are `4` and `1/4`.
- The unit circle maps to an ellipse with semiaxes `4` and `1/4`.
- The inverse singular values are `1/4` and `4`.
- Equal output perturbations produce inverse responses with norms
  `epsilon/4` and `4 epsilon`.
- The response ratio and two-norm condition number are both `16`.
- As the smallest singular value approaches zero, the condition number tends
  to infinity.

## Story

1. Present a map that is one-to-one and onto but unevenly sensitive.
2. Identify its strong and weak singular directions.
3. Show the unit circle becoming a long, thin ellipse.
4. Reciprocate the singular values to form the inverse stretches.
5. Compare equal perturbations in the two output directions.
6. Calculate the sixteenfold difference in inverse response.
7. Define the two-norm condition number.
8. State the relative-error amplification bound.
9. Connect a shrinking minimum singular value to instability and singularity.
10. Finish by contrasting existence of an inverse with reliability of inversion.

## Architecture

`SVDConditioning` provides singular values, inverse singular values, the
two-norm condition number, singular directions, directional inverse responses,
and the standard relative-error bound. It is independent of Manim.

## Scope boundary

This checkpoint does not introduce truncated SVD, Eckart–Young approximation,
image compression, or PCA. Those remain later topics.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp219_svd_conditioning.zsh
scripts/render_cp219_svd_conditioning.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/svd_conditioning.py
scenes/svd_conditioning_presentation.py
tests/test_svd_conditioning.py
tests/test_svd_conditioning_presentation.py
scripts/check_cp219_svd_conditioning.zsh
scripts/render_cp219_svd_conditioning.zsh
CHECKPOINT_219.md
apply_checkpoint_219.zsh
```
