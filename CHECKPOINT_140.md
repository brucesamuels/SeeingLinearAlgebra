# Checkpoint 140 — Determinant and Invertibility

## Purpose

CP140 moves from determinant computation to determinant meaning. The determinant becomes a test for invertibility of a square matrix.

## Mathematical narrative

1. Use an invertible triangular matrix with determinant 24. Connect the nonzero determinant to three pivots, rank 3, trivial null space, and invertibility.
2. Contrast with a singular matrix whose second row is twice the first. Its determinant is zero.
3. Exhibit an explicit nonzero null vector, showing that information is lost and the matrix cannot be inverted.
4. Interpret the determinant geometrically: nonzero determinant preserves dimension and scales signed volume; zero determinant collapses dimension and volume.
5. Assemble the equivalence chains only after the concrete examples have been seen.

For an n x n matrix:

\[
\det(A)\neq0
\Longleftrightarrow
\text{a pivot in every row and column}
\Longleftrightarrow
\operatorname{rank}(A)=n
\Longleftrightarrow
\mathcal N(A)=\{\mathbf0\}
\Longleftrightarrow
A\text{ invertible}.
\]

The zero-determinant/singular chain is displayed in parallel.

## Files

- `engine/determinant_invertibility.py`
- `scenes/determinant_invertibility_presentation.py`
- `tests/test_determinant_invertibility.py`
- `tests/test_determinant_invertibility_presentation.py`
- `tests/test_cp140_scripts.py`
- `scripts/check_cp140_invertibility.zsh`
- `scripts/render_cp140_invertibility.zsh`


## R2 refinement — formal null-space criterion

Added a dedicated theorem card stating formally, for a square matrix,

\[
A\text{ is invertible}\iff\mathcal N(A)=\{\mathbf0\}.
\]

The same card restates this as: the homogeneous system \(A\mathbf x=\mathbf0\) has only the trivial solution \(\mathbf x=\mathbf0\). The card appears before the broader equivalence chains so the null-space criterion is explicit rather than merely embedded in a list of equivalent conditions.
