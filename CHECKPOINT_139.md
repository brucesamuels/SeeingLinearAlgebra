# Checkpoint 139 — Determinants of Triangular and Block-Triangular Matrices

## Purpose

CP139 develops a structural shortcut for determinant computation. Students first see that an upper triangular matrix has determinant equal to the product of its diagonal entries. The lesson then explains why this follows recursively from cofactor expansion, confirms the same rule for lower triangular matrices, and extends the idea to block-triangular matrices.

## Student-facing sequence

1. Recognize an upper triangular matrix.
2. Highlight the diagonal and compute its determinant by the diagonal product.
3. Explain the rule with recursive cofactor expansion on a symbolic 3x3 upper triangular matrix.
4. Confirm that lower triangular matrices obey the same rule.
5. Introduce the block-triangular identity
   \[
   \det\begin{bmatrix}A&B\\0&D\end{bmatrix}=\det(A)\det(D).
   \]
6. End with the strategy: recognize structure before doing a long computation.

## Files

- `engine/determinant_triangular.py`
- `scenes/determinant_triangular_presentation.py`
- `tests/test_determinant_triangular.py`
- `tests/test_determinant_triangular_presentation.py`
- `tests/test_cp139_scripts.py`
- `scripts/check_cp139_triangular.zsh`
- `scripts/render_cp139_triangular.zsh`
