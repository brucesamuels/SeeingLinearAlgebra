# Seeing Linear Algebra — Checkpoint 116

## Topic
Building a basis for the null space from special solutions.

## Goal
Use the rank-one homogeneous system from CP115 to formalize Strang's method:
construct one special solution for each free variable, verify that the special
solutions lie in the null space, show that they span the null space, prove that
they are independent, and conclude that they form a basis.

## Mathematical content
Start with

\[
\left[
\begin{array}{ccc|c}
1&2&-1&0\\
0&0&0&0\\
0&0&0&0
\end{array}
\right].
\]

The equation is

\[
x+2y-z=0,
\]

with free variables \(y\) and \(z\).

### First special solution
Set

\[
y=1,
\qquad z=0.
\]

Then \(x=-2\), so

\[
\mathbf{s}_1=
\begin{bmatrix}-2\\1\\0\end{bmatrix}.
\]

### Second special solution
Set

\[
y=0,
\qquad z=1.
\]

Then \(x=1\), so

\[
\mathbf{s}_2=
\begin{bmatrix}1\\0\\1\end{bmatrix}.
\]

### Membership
Verify

\[
A\mathbf{s}_1=\mathbf{0},
\qquad
A\mathbf{s}_2=\mathbf{0}.
\]

### Spanning
Let \(y=s\) and \(z=t\). Then

\[
x=-2s+t,
\]

so every null-space solution is

\[
\mathbf{x}=
 s\begin{bmatrix}-2\\1\\0\end{bmatrix}
+t\begin{bmatrix}1\\0\\1\end{bmatrix}.
\]

Thus

\[
N(A)=\operatorname{span}\{\mathbf{s}_1,\mathbf{s}_2\}.
\]

### Independence
If

\[
c_1\mathbf{s}_1+c_2\mathbf{s}_2=\mathbf{0},
\]

then the second coordinate gives \(c_1=0\), and the third coordinate gives
\(c_2=0\). Therefore the special solutions are independent.

Hence

\[
\mathcal B_{N(A)}=
\left\{
\begin{bmatrix}-2\\1\\0\end{bmatrix},
\begin{bmatrix}1\\0\\1\end{bmatrix}
\right\},
\qquad
\dim N(A)=2.
\]

## Pedagogical sequence
1. Identify the pivot and free variables.
2. Ask how many special solutions two free variables should produce.
3. Set one free variable to 1 and the other to 0, one at a time.
4. Verify that both special solutions lie in the null space.
5. Show that they span every null-space solution.
6. Prove independence by reading the second and third coordinates.
7. Conclude that the special solutions form a basis.
8. Visualize the null space as a plane through the origin in \(\mathbb R^3\).
9. Connect free-variable count, basis size, and nullity.

## Files
```text
engine/null_space_basis.py
scenes/null_space_basis_presentation.py
tests/test_null_space_basis.py
tests/test_null_space_basis_presentation.py
scripts/check_cp116_null_space_basis.zsh
scripts/render_cp116_null_space_basis.zsh
CHECKPOINT_116.md
```

## Visual review targets
- Variable labels align directly over their matrix columns.
- The two special-solution cards remain balanced and readable.
- Membership, spanning, and independence appear as three distinct checks.
- The basis panel and plane visualization do not collide.
- The final pattern screen stays comfortably inside the frame.


## Revision 1 layout refinement
The rendered video showed repeated collisions between each scene heading and a redundant heading inside several large panels. The special-solution, membership, spanning, independence, and summary panels now omit those duplicate internal headings. Their mathematical content is lowered slightly and remains enclosed within the yellow border.
