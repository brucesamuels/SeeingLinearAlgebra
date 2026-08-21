# Checkpoint 181 — Solving a First-Order System with Eigenvectors

CP181 applies the eigenvalue/eigenvector machinery to the coupled system

\[\mathbf x'(t)=A\mathbf x(t),\qquad A=\begin{bmatrix}3&1\\1&3\end{bmatrix}.\]

The lesson derives the ansatz \(\mathbf x=e^{\lambda t}\mathbf v\), obtains the eigenvalue equation \(A\mathbf v=\lambda\mathbf v\), forms the general solution from the two eigenmodes, applies \(\mathbf x(0)=(2,0)^T\), and visualizes the long-term alignment with the dominant eigendirection. The final card reframes the method as a coordinate change that decouples the vector system into independent scalar ODEs.


## Revision note

This revision lowers and slightly compacts the Card 4 initial-condition block so the orange initial-condition expression no longer collides with the subheading.
