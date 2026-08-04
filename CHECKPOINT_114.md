# Seeing Linear Algebra — Checkpoint 114

## Topic
Pivot variables, free variables, the parameter method, and Strang's
particular-plus-special-solution viewpoint.

## Goal
Start from an RREF system with one free variable. Identify pivot and free
variables, then show two equivalent ways to describe the infinite solution set:

1. the standard textbook parameter method; and
2. Strang's method of combining a particular solution with a special solution.

## Mathematical content
Use the RREF system

\[
\left[
\begin{array}{ccc|c}
1&0&2&4\\
0&1&-1&1\\
0&0&0&0
\end{array}
\right].
\]

This gives

\[
x+2z=4,
\qquad
y-z=1,
\]

with \(z\) free.

### Textbook method
Set

\[
z=t.
\]

Then

\[
x=4-2t,
\qquad
y=1+t,
\qquad z=t,
\]

so

\[
\begin{bmatrix}x\\y\\z\end{bmatrix}
=
\begin{bmatrix}4\\1\\0\end{bmatrix}
+t\begin{bmatrix}-2\\1\\1\end{bmatrix}.
\]

### Strang's viewpoint
Set the free variable to \(0\) to obtain a particular solution:

\[
\begin{bmatrix}4\\1\\0\end{bmatrix}.
\]

Set the free variable to \(1\) to obtain the special solution:

\[
\begin{bmatrix}-2\\1\\1\end{bmatrix}.
\]

Then every solution is

\[
\text{particular solution} + t(\text{special solution}).
\]

## Pedagogical sequence
1. Show the RREF matrix and identify pivot vs free variables.
2. Present the textbook parameter method.
3. Write the parametric vector form.
4. Reinterpret the same result using Strang's viewpoint.
5. Obtain the particular solution by setting the free variable to zero.
6. Obtain the special solution by setting the free variable to one.
7. Summarize that the two descriptions represent the same solution set.

## Files
```text
engine/pivot_and_free_variables.py
scenes/pivot_and_free_variables_presentation.py
tests/test_pivot_and_free_variables.py
tests/test_pivot_and_free_variables_presentation.py
scripts/check_cp114_pivot_and_free_variables.zsh
scripts/render_cp114_pivot_and_free_variables.zsh
CHECKPOINT_114.md
```

## Visual review targets
- The matrix and right-side panel stay comfortably separated.
- Pivot and free-column highlights are clear.
- The textbook method panel reads cleanly in the available space.
- The Strang cards for \(z=0\) and \(z=1\) are balanced and readable.
- The final comparison screen makes the equivalence of the two viewpoints obvious.
