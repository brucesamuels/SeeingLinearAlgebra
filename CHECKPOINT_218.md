# Checkpoint 218 — Least Squares and Minimum-Norm Solutions

This lesson applies the pseudoinverse to a target outside the image of a
rank-deficient map. It separates the closest reachable output from the choice
of pre-image and shows why the pseudoinverse solution has minimum norm.

## Numerical spine

Reuse

```text
A=[[1,1],
   [1,1],
   [0,0]],
```

and choose `b=(3,1,2)`.

- `b` is not in the image of `A`, so `Ax=b` is inconsistent.
- `AA^+b=(2,2,0)` is the closest reachable output.
- The residual is `(1,-1,2)` and satisfies `A^T r=0`.
- `A^+b=(1,1)` is a pre-image of the projected output.
- Every least-squares solution is `(1,1)+t(1,-1)`.
- Its squared norm is `2+2t^2`, uniquely minimized at `t=0`.

## Story

1. Present a target outside the image and explain that it has no pre-image.
2. Make the inconsistent component equations explicit.
3. Separate the closest-output question from the selected-pre-image question.
4. Compute `AA^+b`, the projection onto the image.
5. Verify that the residual is orthogonal to every reachable output.
6. Compute `A^+b`, the row-space pre-image.
7. Display the full family of pre-images created by null-space motion.
8. Prove that the pseudoinverse choice uniquely minimizes the norm.
9. Interpret `A` as a bijection from row space to image, with `A^+` as its inverse.
10. Finish with `A^+b` as the minimum-norm least-squares solution.

## Architecture

`PseudoinverseLeastSquares` composes the CP217 `SVDPseudoinverse` model. It
provides the projected output, orthogonal residual, pseudoinverse solution,
null-space solution family, residual error, and solution norm without depending
on Manim.

## Scope boundary

This checkpoint does not introduce condition numbers, truncated SVD,
Eckart–Young approximation, image compression, or PCA.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp218_pseudoinverse_least_squares.zsh
scripts/render_cp218_pseudoinverse_least_squares.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/pseudoinverse_least_squares.py
scenes/pseudoinverse_least_squares_presentation.py
tests/test_pseudoinverse_least_squares.py
tests/test_pseudoinverse_least_squares_presentation.py
scripts/check_cp218_pseudoinverse_least_squares.zsh
scripts/render_cp218_pseudoinverse_least_squares.zsh
CHECKPOINT_218.md
apply_checkpoint_218.zsh
```
