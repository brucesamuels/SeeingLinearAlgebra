# Checkpoint 121: Multiple Right-Hand Sides

## Purpose

Solve several systems with one coefficient matrix by writing

\[
AX=B,
\]

then compare independent row reductions with one block reduction and one reusable LU factorization.

## Mathematical example

\[
A=\begin{bmatrix}
2&1&1\\
4&-6&0\\
-2&7&2
\end{bmatrix},
\qquad
B=\begin{bmatrix}
3&0\\
4&-6\\
0&5
\end{bmatrix}.
\]

The solution matrix is

\[
X=\begin{bmatrix}
1&0\\
0&1\\
1&-1
\end{bmatrix}.
\]

The same three elimination operations act across the entire block \([A\mid B]\), producing

\[
[U\mid Y],
\quad
U=\begin{bmatrix}
2&1&1\\
0&-8&-2\\
0&0&1
\end{bmatrix},
\quad
Y=\begin{bmatrix}
3&0\\
-2&-6\\
1&-1
\end{bmatrix}.
\]

With

\[
A=LU,
\quad
L=\begin{bmatrix}
1&0&0\\
2&1&0\\
-1&-1&1
\end{bmatrix},
\]

the two triangular systems are

\[
LY=B,
\qquad
UX=Y.
\]

## Operation-count comparison

Using the convention that each scalar addition, subtraction, multiplication, or division counts as one operation:

- factor the 3 by 3 matrix: 13 operations;
- forward substitution per right-hand side: 6 operations;
- back substitution per right-hand side: 9 operations;
- total triangular work per right-hand side: 15 operations.

For two right-hand sides:

\[
\text{two independent reductions}=2(13+15)=56,
\]

while

\[
\text{factor once, solve twice}=13+2(15)=43.
\]

The saving is 13 operations: one unnecessary factorization.

For an n by n matrix and m right-hand sides, the leading-order comparison is

\[
m\left(\frac23n^3+2n^2\right)
\]

versus

\[
\frac23n^3+2mn^2.
\]

Block elimination and LU reuse have the same arithmetic count when all columns of B are available at once. LU is more reusable because future right-hand sides require only forward and back substitution.

## Files

- `engine/multiple_right_hand_sides.py`
- `scenes/multiple_right_hand_sides_presentation.py`
- `tests/test_multiple_right_hand_sides.py`
- `tests/test_multiple_right_hand_sides_presentation.py`
- `scripts/check_cp121_multiple_right_hand_sides.zsh`
- `scripts/render_cp121_multiple_right_hand_sides.zsh`

## Validation

Run:

```zsh
./scripts/check_cp121_multiple_right_hand_sides.zsh
```

Render:

```zsh
./scripts/render_cp121_multiple_right_hand_sides.zsh
```


## Revised timing

The presentation uses longer card transitions and row-highlight animations while preserving the approved layout and reading pauses.
