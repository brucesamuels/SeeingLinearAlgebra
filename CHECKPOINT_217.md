# Checkpoint 217 — The Pseudoinverse: Undo What Can Be Undone

This lesson continues the rank-deficient SVD sequence by constructing the
pseudoinverse. Because the running matrix is rectangular and loses a direction,
an ordinary inverse cannot exist. The pseudoinverse reverses the positive
singular stretch and leaves every zero singular value at zero.

## Numerical spine

Reuse

```text
A=[[1,1],
   [1,1],
   [0,0]],
```

with singular values `2` and `0`.

- `Sigma^+` is the 2-by-3 matrix with first entry `1/2` and all others zero.
- `A^+=V Sigma^+ U^T` maps `R^3` back to `R^2`.
- `A^+=(1/4)[[1,1,0],[1,1,0]]`.
- `A^+ A v_1=v_1`, but `A^+ A v_2=0`.
- `A^+ A` is projection onto the row space.
- `A A^+` is projection onto the column space.

## Story

1. Explain why a rectangular, information-losing matrix has no ordinary inverse.
2. Recall the active singular lane and the zero singular lane.
3. Pause and ask what should happen to zero when the SVD is reversed.
4. Define the zero-safe reciprocal rule for singular values.
5. Construct the dimension-reversing `Sigma^+`.
6. Reverse the orthogonal factors to obtain `A^+=V Sigma^+ U^T`.
7. Display the explicit two-by-three pseudoinverse.
8. Contrast exact recovery of `v_1` with permanent loss of `v_2`.
9. Interpret `A^+ A` and `A A^+` as orthogonal projections.
10. Finish with the principle: undo exactly the information that `A` preserves.

## Architecture

`SVDPseudoinverse` composes the CP216 `SVDFundamentalSubspaces` model and adds
the reciprocal singular-value matrix, pseudoinverse, forward and reverse maps,
round trips, and the row- and column-space projectors. It has no renderer
dependency.

## Scope boundary

This checkpoint does not yet use `A^+b` as a least-squares or minimum-norm
solution formula. Normal equations, conditioning, approximation, image
compression, and PCA remain later topics.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp217_svd_pseudoinverse.zsh
scripts/render_cp217_svd_pseudoinverse.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/svd_pseudoinverse.py
scenes/svd_pseudoinverse_presentation.py
tests/test_svd_pseudoinverse.py
tests/test_svd_pseudoinverse_presentation.py
scripts/check_cp217_svd_pseudoinverse.zsh
scripts/render_cp217_svd_pseudoinverse.zsh
CHECKPOINT_217.md
apply_checkpoint_217.zsh
```
