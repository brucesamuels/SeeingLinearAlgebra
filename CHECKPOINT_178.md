# Checkpoint 178 — Symmetric Matrices and Orthogonal Eigenvectors

This lesson begins the transition from general diagonalization to the spectral theorem.

It uses the symmetric matrix

\[
A=\begin{bmatrix}2&1\\1&2\end{bmatrix}
\]

with eigenpairs

\[
\lambda_1=3,\quad \mathbf v_1=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\lambda_2=1,\quad \mathbf v_2=\begin{bmatrix}1\\-1\end{bmatrix}.
\]

The presentation first makes the orthogonality visible geometrically and verifies \(\mathbf v_1^T\mathbf v_2=0\). It then proves the general result for a real symmetric matrix \(A\): if

\[
A\mathbf v=\lambda\mathbf v,
\qquad
A\mathbf w=\mu\mathbf w,
\qquad
\lambda\ne\mu,
\]

then symmetry gives

\[
\mathbf v^TA\mathbf w=(A\mathbf v)^T\mathbf w.
\]

Comparing the two evaluations yields

\[
(\lambda-\mu)\mathbf v^T\mathbf w=0,
\]

so \(\mathbf v^T\mathbf w=0\).

The final cards normalize the eigenvectors, form an orthogonal eigenvector matrix \(Q\), and preview the spectral theorem:

\[
Q^{-1}=Q^T,
\qquad
D=Q^TAQ,
\qquad
A=QDQ^T.
\]
