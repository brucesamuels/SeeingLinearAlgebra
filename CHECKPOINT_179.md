# Checkpoint 179 — The Spectral Theorem

This checkpoint develops the spectral theorem for real symmetric matrices as the synthesis of CP178.

## Mathematical arc

1. Recall the symmetric matrix and orthonormal eigenvector matrix from CP178.
2. Compute the diagonal matrix algebraically as `D = Q^T A Q`.
3. Rearrange to obtain `A = Q D Q^T`.
4. Verify the factorization numerically with the running 2x2 example.
5. Interpret the factors geometrically: move into the orthonormal eigenbasis, scale independently, move back.
6. State the spectral theorem for real symmetric matrices.
7. Close with why orthogonal diagonalization matters and preview later applications.

## Running example

A = [[2,1],[1,2]]

Q = (1/sqrt(2)) [[1,1],[1,-1]]

D = Q^T A Q = [[3,0],[0,1]]

A = Q D Q^T.

## Preview

Render with:

`zsh scripts/render_cp179_spectral_theorem.zsh`


## Revision note

The final card now renders the inverse and transpose notation with MathTex, so `Q^{-1}` and `Q^T` display correctly instead of appearing as unresolved LaTeX inside plain text.
