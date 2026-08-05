# Checkpoint 123: Why Some Matrices Are Not Invertible

## Purpose

Contrast CP122 with a singular matrix.  Attempt Gauss-Jordan inversion on
`[A | I]`, show why the left side cannot become `I`, and connect the failed
pivot structure to the null space, dependent columns, and unit-vector systems
that are not all solvable.

## Mathematics

The fixed matrix is

\[
A=\begin{bmatrix}
1&2&1\\
2&4&2\\
0&1&1
\end{bmatrix}.
\]

Its row reduction produces

\[
\left[
\begin{array}{ccc|ccc}
1&0&-1&1&0&-2\\
0&1&1&0&0&1\\
0&0&0&-2&1&0
\end{array}
\right].
\]

The missing third pivot gives

\[
\operatorname{rank}(A)=2<3,
\]

so the left block cannot become the identity.  The final right-hand row also
shows that `A x = e_1` and `A x = e_2` are inconsistent, while `A x = e_3`
has infinitely many solutions.  Therefore `AX=I` has no solution.

The homogeneous system gives

\[
N(A)=\operatorname{span}\left\{
\begin{bmatrix}1\\-1\\1\end{bmatrix}
\right\},
\]

and hence

\[
\mathbf c_1-\mathbf c_2+\mathbf c_3=\mathbf0.
\]

The lesson closes with the equivalent invertibility tests based on pivots,
rank, null space, and unique solvability for every right-hand side.

## Files

- `engine/noninvertible_matrix.py`
- `scenes/noninvertible_matrix_presentation.py`
- `tests/test_noninvertible_matrix.py`
- `tests/test_noninvertible_matrix_presentation.py`
- `scripts/check_cp123_noninvertible_matrix.zsh`
- `scripts/render_cp123_noninvertible_matrix.zsh`


## Import-path safeguard

The focused check and render scripts explicitly add the repository root to `PYTHONPATH` before invoking Python or Manim. This ensures that the scene can import `engine.noninvertible_matrix` regardless of how the Manim launcher initializes `sys.path`.

## Layout refinement

The null-space panel is positioned relative to its heading with an explicit
vertical buffer. This prevents the sentence “The missing pivot creates a
nonzero null-space vector” from overlapping the surrounding box.
