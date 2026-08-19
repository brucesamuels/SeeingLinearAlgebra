# Checkpoint 173 — Computing Eigenvectors

## Purpose

Continue the Chapter 7 eigenvalue/eigenvector sequence immediately after CP172. CP172 found the eigenvalues

\[
\lambda=1,2,5
\]

for

\[
A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}.
\]

CP173 now computes an eigenspace for each eigenvalue by solving

\[
(A-\lambda I)\mathbf v=\mathbf0.
\]

## Mathematical results

- \(\lambda=1\):
  \[
  E_1=\operatorname{span}\left\{\begin{bmatrix}0\\0\\1\end{bmatrix}\right\}.
  \]
- \(\lambda=2\):
  \[
  E_2=\operatorname{span}\left\{\begin{bmatrix}1\\-2\\0\end{bmatrix}\right\}.
  \]
- \(\lambda=5\):
  \[
  E_5=\operatorname{span}\left\{\begin{bmatrix}1\\1\\0\end{bmatrix}\right\}.
  \]

The scene directly verifies the \(\lambda=2\) case in the defining equation \(A\mathbf v=\lambda\mathbf v\).

## Pedagogy

The three eigenvalue cases are presented in parallel, fully worked form. The lesson deliberately reuses the CP172 matrix so that students see the computational sequence as one continuous method:

1. find an eigenvalue;
2. substitute it into \(A-\lambda I\);
3. solve the homogeneous system;
4. express the solution as a span;
5. interpret all nonzero vectors in that span as eigenvectors.

## Validation

The focused checker compiles the engine, presentation, and tests and then runs the two CP173 test files.


## Revision note

This CP173 revision lowers the worked matrix blocks across the lesson, tightens the header/subheader stack, and uses explicit content placement below each heading so matrices no longer collide with the upper text bands.


## Null-space emphasis revision

The lesson now explicitly frames each eigenvector computation as finding the null space of `A - lambda I`. Each worked case displays `E_lambda = Null(A - lambda I)` before solving the corresponding homogeneous system.


## Revision note

This revision makes the null-space computation explicit and line-by-line for each eigenvalue. For λ=1, 2, and 5, the scene now shows the full matrix subtraction A-λI, the homogeneous matrix equation, and the algebra revealed step by step before identifying the eigenspace.


## Final-card revision

The lesson now closes by collecting the three independent eigenvectors and stating explicitly that they form an eigenvector basis for \(\mathbb R^3\). This prepares the transition from eigenspaces to eigenvector coordinates and diagonalization.
