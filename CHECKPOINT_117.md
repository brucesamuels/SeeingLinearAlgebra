# Seeing Linear Algebra — Checkpoint 117

## Topic
The complete solution of a consistent linear system.

## Goal
Connect the particular solution of a nonhomogeneous system with the null-space
basis from CP116 and establish the complete-solution form

\[
\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n.
\]

## Mathematical example
Use

\[
\left[
\begin{array}{ccc|c}
1&2&-1&3\\
0&0&0&0\\
0&0&0&0
\end{array}
\right].
\]

Setting the free variables equal to zero gives one particular solution:

\[
\mathbf{x}_p=
\begin{bmatrix}3\\0\\0\end{bmatrix}.
\]

The associated homogeneous system has null-space basis

\[
\mathbf{s}_1=
\begin{bmatrix}-2\\1\\0\end{bmatrix},
\qquad
\mathbf{s}_2=
\begin{bmatrix}1\\0\\1\end{bmatrix}.
\]

Thus

\[
\mathbf{x}_n=
 s\begin{bmatrix}-2\\1\\0\end{bmatrix}
+t\begin{bmatrix}1\\0\\1\end{bmatrix},
\]

and the complete solution is

\[
\mathbf{x}=
\begin{bmatrix}3\\0\\0\end{bmatrix}
+s\begin{bmatrix}-2\\1\\0\end{bmatrix}
+t\begin{bmatrix}1\\0\\1\end{bmatrix}.
\]

## Why the formula works
Since

\[
A\mathbf{x}_p=\mathbf{b}
\qquad\text{and}\qquad
A\mathbf{x}_n=\mathbf{0},
\]

we have

\[
A(\mathbf{x}_p+\mathbf{x}_n)
=A\mathbf{x}_p+A\mathbf{x}_n
=\mathbf{b}+\mathbf{0}
=\mathbf{b}.
\]

Conversely, if \(A\mathbf{x}=\mathbf{b}\), then

\[
A(\mathbf{x}-\mathbf{x}_p)=\mathbf{0},
\]

so \(\mathbf{x}-\mathbf{x}_p\in N(A)\). Therefore every solution has the form

\[
\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n.
\]

## Geometric interpretation
The null space is a plane through the origin. Adding \(\mathbf{x}_p\) translates
that plane without changing its directions. The nonhomogeneous solution set is
therefore an affine plane parallel to \(N(A)\) and passing through
\(\mathbf{x}_p\).

## Pedagogical sequence
1. Introduce the two-part structure of the complete solution.
2. Find a particular solution by setting the free variables to zero.
3. Recall the null-space basis from CP116.
4. Combine the particular and null-space parts.
5. Verify that every vector in the formula solves the system.
6. Prove that every solution must have this form.
7. Visualize the nonhomogeneous solution set as a translation of the null space.
8. Summarize the reusable procedure.

## Files
```text
engine/complete_solution.py
scenes/complete_solution_presentation.py
tests/test_complete_solution.py
tests/test_complete_solution_presentation.py
scripts/check_cp117_complete_solution.zsh
scripts/render_cp117_complete_solution.zsh
CHECKPOINT_117.md
```

## Visual review targets
- Scene headings should remain clearly above their boxes.
- The complete solution should visibly separate the particular and null-space parts.
- The verification and converse arguments should have generous vertical spacing.
- The translated plane should be visibly parallel to the null-space plane.
- All text must remain inside the frame and free of collisions.

## Revision note
The combine-panel column vectors use explicit LaTeX row separators (`\\`) and are covered by a regression test.
