# Seeing Linear Algebra — Checkpoint 105 (revised)

## What Does It Mean to Solve \(A\mathbf{x}=\mathbf{b}\)?

## Goal

Open the linear-systems chapter by presenting the idea of a solution in two
stages:

1. a two-dimensional scaffold in which two lines intersect at one point;
2. a three-dimensional extension in which three planes meet at one point;
3. the system of equations;
4. the matrix equation \(A\mathbf{x}=\mathbf{b}\);
5. a linear combination of the columns of \(A\).

The lesson establishes the problem that elimination will solve. It does not yet
introduce row operations, Gaussian elimination, echelon form, or augmented
matrices.

## Mathematical examples

### Opening 2D scaffold

\[
\begin{aligned}
x+y&=2,\\
x-y&=0.
\end{aligned}
\]

The two lines intersect at

\[
(x,y)=(1,1).
\]

### Main 3D example

\[
\begin{aligned}
x+y+z&=3,\\
2x-y+z&=2,\\
x+2y-z&=2.
\end{aligned}
\]

The coefficient matrix has determinant \(7\), so the system has the unique
solution

\[
(x,y,z)=(1,1,1).
\]

The matrix form is

\[
\begin{bmatrix}
1&1&1\\
2&-1&1\\
1&2&-1
\end{bmatrix}
\begin{bmatrix}x\\y\\z\end{bmatrix}
=
\begin{bmatrix}3\\2\\2\end{bmatrix}.
\]

The column interpretation is

\[
x\begin{bmatrix}1\\2\\1\end{bmatrix}
+y\begin{bmatrix}1\\-1\\2\end{bmatrix}
+z\begin{bmatrix}1\\1\\-1\end{bmatrix}
=\begin{bmatrix}3\\2\\2\end{bmatrix}.
\]

## Pedagogical sequence

1. Show two lines in \(\mathbb R^2\) and their intersection.
2. Label that point as the solution \((1,1)\).
3. Transition to \(\mathbb R^3\): three planes with one common point.
4. Label the common point \((1,1,1)\).
5. Replace the geometry with equations and the matrix equation.
6. Ask what the entries of \(\mathbf{x}\) control.
7. Isolate the matrix equation and animate all three row-by-column products with matching color highlights.
8. Reveal the column-combination interpretation.
9. Conclude that solving \(A\mathbf{x}=\mathbf{b}\) means finding the
   coefficients that combine the columns of \(A\) to produce \(\mathbf{b}\).

## Responsibility boundary

`engine/linear_system_meaning.py` owns:

- validated 2D and 3D system data;
- the unique solutions;
- columns and weighted columns for the 3D system;
- reconstruction of \(\mathbf b\);
- residual, line-membership, and plane-membership calculations;
- line and plane height calculations for the selected examples.

The Manim scene owns:

- line, plane, axis, equation, and matrix construction;
- camera movement;
- layout and typography;
- prediction and reflection timing;
- transitions from 2D intuition to 3D structure to algebraic viewpoints.

The engine performs no Manim construction. The scene performs no solving or
column arithmetic.

## Files

```text
engine/linear_system_meaning.py
scenes/linear_system_meaning_presentation.py
tests/test_linear_system_meaning.py
tests/test_linear_system_meaning_presentation.py
scripts/check_cp105_linear_system_meaning.zsh
scripts/render_cp105_linear_system_meaning.zsh
CHECKPOINT_105.md
```

## Visual review targets

- The 2D opening reads clearly before the 3D transition begins.
- The title remains comfortably within the frame.
- Plane transparency allows all three planes and the common point to remain
  visible.
- The intersection point is visually unmistakable in both 2D and 3D.
- The equation and matrix panels do not collide with the title or each other.
- The column-combination formula fits within the horizontal safe area.
- Every text-heavy frame remains on screen long enough to read.
- No checkpoint terminology appears in the student-facing scene.

## Next checkpoint

CP106 should introduce the augmented matrix and carefully explain what
information is preserved when the variable names and equality signs are
suppressed.
