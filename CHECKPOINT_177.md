# Checkpoint 177 — Repeated Eigenvalues and Diagonalizability

## Purpose

Show that a repeated eigenvalue does not determine diagonalizability. What matters is whether its eigenspace contains enough independent eigenvectors.

## Mathematical contrast

Use two matrices with the same characteristic polynomial:

- `A1 = [[2,0],[0,2]]`, with `E_2 = R^2`, geometric multiplicity 2, diagonalizable.
- `A2 = [[2,1],[0,2]]`, with `E_2 = span{(1,0)}`, geometric multiplicity 1, not diagonalizable.

Both have `(2-lambda)^2`, so the eigenvalue 2 has algebraic multiplicity 2 in each case.

## Lesson arc

1. Same repeated characteristic root, two matrices.
2. Compute the eigenspace of `A1`.
3. Compute the eigenspace of `A2`.
4. Compare eigenspace dimensions directly.
5. Introduce algebraic and geometric multiplicity.
6. State the diagonalizability criterion.
7. Conclude: repeated eigenvalues are not the problem; missing eigenvectors are.

## Visual intent

Keep the lesson primarily 2D and matrix-centered. Use green for the diagonalizable example, orange/red for the defective example, and yellow for structural conclusions. Maintain generous vertical spacing beneath headings.
