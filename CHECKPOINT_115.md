# Seeing Linear Algebra — Checkpoint 115

## Topic
Homogeneous systems, the null space, and the role of special solutions.

## Goal
Start with a homogeneous system that has one free variable and show that its
solutions form the null space. Then extend the lesson with a rank-one example
that has two free variables, so students can explicitly see one particular
solution together with two special solutions.

## Mathematical content
### Part A: a homogeneous system
Use

\[
\left[
\begin{array}{ccc|c}
1&0&2&0\\
0&1&-1&0\\
0&0&0&0
\end{array}
\right],
\]

which gives

\[
x+2z=0,
\qquad y-z=0.
\]

Set \(z=t\). Then

\[
x=-2t,
\qquad y=t,
\qquad z=t,
\]

so

\[
\mathbf{x}=t\begin{bmatrix}-2\\1\\1\end{bmatrix}.
\]

The special solution is obtained by setting \(t=1\):

\[
\mathbf{s}=\begin{bmatrix}-2\\1\\1\end{bmatrix}.
\]

Therefore

\[
N(A)=\operatorname{span}\left\{\begin{bmatrix}-2\\1\\1\end{bmatrix}\right\}.
\]

### Part B: a rank-one system with two free variables
Use

\[
\left[
\begin{array}{ccc|c}
1&2&-1&3\\
0&0&0&0\\
0&0&0&0
\end{array}
\right],
\]

which gives

\[
x+2y-z=3.
\]

Set

\[
y=s,
\qquad z=t.
\]

Then

\[
x=3-2s+t.
\]

So the full solution set is

\[
\mathbf{x}=\underbrace{\begin{bmatrix}3\\0\\0\end{bmatrix}}_{\text{particular solution}}
+s\underbrace{\begin{bmatrix}-2\\1\\0\end{bmatrix}}_{\text{special solution 1}}
+t\underbrace{\begin{bmatrix}1\\0\\1\end{bmatrix}}_{\text{special solution 2}}.
\]

This makes explicit that a nonhomogeneous system is described by

\[
\mathbf{x}=\mathbf{x}_p+\text{(null-space combination)}.
\]

## Pedagogical sequence
1. Introduce homogeneous systems and emphasize that \(\mathbf{0}\) always solves \(A\mathbf{x}=\mathbf{0}\).
2. Show that a free variable can produce nonzero solutions.
3. Set the free variable to \(1\) to obtain Strang's special solution.
4. Define the null space and visualize it as a line through the origin.
5. Transition to a rank-one system with two free variables.
6. Solve it by choosing two free variables.
7. Introduce the particular solution explicitly.
8. Identify the two special solutions.
9. Summarize the contrast between homogeneous and nonhomogeneous solution sets.

## Files
```text
engine/homogeneous_null_space.py
scenes/homogeneous_null_space_presentation.py
tests/test_homogeneous_null_space.py
tests/test_homogeneous_null_space_presentation.py
scripts/check_cp115_homogeneous_null_space.zsh
scripts/render_cp115_homogeneous_null_space.zsh
CHECKPOINT_115.md
```

## Visual review targets
- The null-space definition and geometry should remain well separated.
- The homogeneous one-free-variable example should clearly show the line through the origin.
- The rank-one example should clearly identify both free variables.
- The particular solution and the two special solutions should be visually distinct.
- The final comparison should make the structural difference unmistakable.
