# Checkpoint 180 — Dynamics and the Dominant Eigenvector

This lesson closes the main eigenvalue/eigenvector arc by showing how repeated applications of a diagonalizable matrix amplify different eigenvector components at different rates.

Using the symmetric example

\[
A=\begin{bmatrix}3&1\\1&3\end{bmatrix},
\]

with eigenvalues 4 and 2 and orthonormal eigenvectors \(q_1,q_2\), the lesson starts from

\[
x=q_1+q_2
\]

and derives

\[
A^k x=4^kq_1+2^kq_2
=4^k\left(q_1+\left(\frac12\right)^kq_2\right).
\]

Thus the normalized iterates approach the dominant eigendirection. A graphical card shows the normalized directions for \(k=0,1,2,4\) converging toward \(q_1\).

The final card states the general dominant-eigenvalue principle, including the necessary caveat that the starting vector must have a nonzero component in the dominant eigendirection.


## Revision note

Fixed the final-card LaTeX concatenation so the implication separator ends with an explicit space before the following `A^k` term. Added a regression test that rejects the malformed `\quadA` token.
