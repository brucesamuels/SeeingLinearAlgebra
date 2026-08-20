# Checkpoint 175 — Diagonalization

Chapter 7 continues from the eigenvector-basis lesson by deriving the diagonal representation algebraically from the known matrices A and P.

## Lesson goals

- Begin with the original matrix A and the eigenvector basis matrix P.
- Start from AP = PD and solve algebraically for D: D = P^{-1} A P.
- Compute P^{-1} explicitly.
- Evaluate P^{-1} A P step by step and discover that the result is diagonal.
- Only after the calculation, identify the diagonal entries as the eigenvalues corresponding to the columns of P.
- Rearrange D = P^{-1} A P to obtain A = P D P^{-1}.
- Interpret the factorization right-to-left as standard coordinates -> eigenbasis coordinates -> diagonal action -> standard coordinates.

The revision deliberately avoids assuming D from the eigenvalues. The diagonal matrix is found by change of basis and then interpreted.


## Revision note

Headings containing mathematical notation now use MathTex so expressions such as $P^{-1}$ and $A=PDP^{-1}$ render correctly rather than appearing as unresolved LaTeX in plain text.
