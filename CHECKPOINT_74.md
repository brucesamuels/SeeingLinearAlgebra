# Checkpoint 74 — The Column Space of a Matrix

## Goal
Connect span and the subspace test directly to matrix multiplication by showing that every output of a matrix is a linear combination of its columns.

## Lesson sequence
1. Display a 3×3 matrix as three column vectors in R³.
2. Draw the three matrix columns from the origin.
3. Reveal that the third column is dependent: a₃ = a₁ + a₂.
4. Introduce
   `A x = x₁a₁ + x₂a₂ + x₃a₃`.
5. Sweep through several coefficient vectors while the output vector moves continuously.
6. Reveal a field of attainable outputs lying in one tilted plane.
7. Identify
   `col(A) = span{a₁,a₂,a₃}`.
8. Close by verifying the zero, addition, and scalar-multiplication conditions from CP73.

## Mathematical choice
The example matrix has rank 2. Its columns live in R³, but the third column equals the sum of the first two, so the column space is a plane through the origin.

## Files added
- `engine/column_space.py`
- `scenes/column_space_presentation.py`
- `tests/test_column_space.py`
- `tests/test_column_space_presentation.py`
- `scripts/check_column_space.zsh`
- `scripts/render_column_space.zsh`
- `CHECKPOINT_74.md`
