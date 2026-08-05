# Checkpoint 124: Pivoting and `PA = LU`

## Purpose

Extend elimination and LU factorization to matrices whose current row order does
not provide a usable pivot.  The lesson distinguishes two reasons to pivot:

1. an exactly zero pivot makes the next elimination multiplier undefined;
2. a very small pivot can create a large multiplier and amplify roundoff.

## Classroom matrix

\[
A=
\begin{bmatrix}
0&2&1\\
2&2&3\\
4&-2&1
\end{bmatrix}.
\]

The first pivot is zero, although \(\det(A)=8\), so the matrix is invertible.
Swapping the first two rows gives

\[
P=
\begin{bmatrix}
0&1&0\\
1&0&0\\
0&0&1
\end{bmatrix},
\qquad
PA=
\begin{bmatrix}
2&2&3\\
0&2&1\\
4&-2&1
\end{bmatrix}.
\]

Elimination uses

\[
m_{31}=2,
\qquad
m_{32}=-3,
\]

and produces

\[
L=
\begin{bmatrix}
1&0&0\\
0&1&0\\
2&-3&1
\end{bmatrix},
\qquad
U=
\begin{bmatrix}
2&2&3\\
0&2&1\\
0&0&-2
\end{bmatrix}.
\]

Therefore

\[
PA=LU,
\qquad
A=P^TLU.
\]

## Numerical pivoting comparison

For

\[
\widetilde A=
\begin{bmatrix}
10^{-4}&1\\
1&1
\end{bmatrix},
\]

keeping the tiny pivot gives multiplier \(10^4\), whereas swapping rows first
gives multiplier \(10^{-4}\).  The lesson uses this contrast to motivate
partial pivoting: choose the largest available magnitude in the pivot column.

## Files

- `engine/pivoting_pa_lu.py`
- `scenes/pivoting_pa_lu_presentation.py`
- `tests/test_pivoting_pa_lu.py`
- `tests/test_pivoting_pa_lu_presentation.py`
- `scripts/check_cp124_pivoting_pa_lu.zsh`
- `scripts/render_cp124_pivoting_pa_lu.zsh`

## Run focused checks

```zsh
./scripts/check_cp124_pivoting_pa_lu.zsh
```

## Render

```zsh
./scripts/render_cp124_pivoting_pa_lu.zsh
```

## Visual review

Check especially:

- the red box around the zero first pivot;
- the three-matrix permutation panel;
- the horizontal `PA = LU` factorization row;
- the two tiny-pivot comparison cards;
- the gap below the partial-pivoting heading.

## Revision 1

- Render the reconstruction note with mixed `Text` and `MathTex` objects so
  \(P^T\) and \(A=P^TLU\) appear as typeset mathematics rather than literal text.
- Add a presentation regression test for the two mathematical expressions.
