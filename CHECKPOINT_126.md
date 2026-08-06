# Checkpoint 126: Solvability of Overdetermined and Underdetermined Systems

## Purpose

Checkpoint 126 follows the general geometry of rectangular matrices with two
worked classes of systems.  It emphasizes that shape alone never decides
consistency:

\[
A\mathbf{x}=\mathbf b\text{ is consistent}
\iff \mathbf b\in\operatorname{Col}(A)
\iff \operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b]).
\]

## Overdetermined example

\[
A=\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix},
\qquad A:\mathbb R^2\to\mathbb R^3.
\]

The column space is the plane

\[
b_3=b_1+b_2.
\]

For

\[
\mathbf b=\begin{bmatrix}2\\-1\\1\end{bmatrix},
\]

the third equation is compatible with the first two and the unique solution is

\[
\mathbf x=\begin{bmatrix}2\\-1\end{bmatrix}.
\]

For

\[
\mathbf b=\begin{bmatrix}2\\-1\\0\end{bmatrix},
\]

row reduction produces \(0=-1\), so the system is inconsistent.

Because the matrix has full column rank, a compatible right-hand side has one
solution.  Because \(\operatorname{rank}(A)=2<3\), the matrix cannot reach
every vector in \(\mathbb R^3\).

## Underdetermined example

\[
A=\begin{bmatrix}1&0&1\\0&1&1\end{bmatrix},
\qquad A:\mathbb R^3\to\mathbb R^2.
\]

For

\[
\mathbf b=\begin{bmatrix}2\\-1\end{bmatrix},
\]

letting \(z=t\) gives

\[
\mathbf x=
\begin{bmatrix}2\\-1\\0\end{bmatrix}
+t\begin{bmatrix}-1\\-1\\1\end{bmatrix}.
\]

The matrix has full row rank, so every right-hand side in \(\mathbb R^2\) is
reachable.  Its nullity is one, so every solution belongs to an infinite
family.

A second wide matrix,

\[
\widetilde A=\begin{bmatrix}1&0&1\\2&0&2\end{bmatrix},
\]

is rank deficient.  With \(\mathbf b=(1,0)^T\), row reduction gives \(0=-2\).
This demonstrates that \(m<n\) does not by itself guarantee consistency.

## Files

- `engine/rectangular_system_solvability.py`
- `scenes/rectangular_system_solvability_presentation.py`
- `tests/test_rectangular_system_solvability.py`
- `tests/test_rectangular_system_solvability_presentation.py`
- `scripts/check_cp126_rectangular_system_solvability.zsh`
- `scripts/render_cp126_rectangular_system_solvability.zsh`

## Validation

Run:

```zsh
./scripts/check_cp126_rectangular_system_solvability.zsh
```

Render:

```zsh
./scripts/render_cp126_rectangular_system_solvability.zsh
```

The next checkpoint will rebuild the complete chapter with CP125 and CP126 in
the appropriate conceptual position.


## Revised 2

- Imports the Manim corner constants used by the perspective output-space frame.
- Adds a runtime construction test for the three-dimensional output-space helper.


## Revision 3

The overdetermined geometry panel now shows coordinate axes and a representative input vector \(\mathbf{x}\) inside the \(\mathbb{R}^2\) domain rather than leaving the input space visually empty.
