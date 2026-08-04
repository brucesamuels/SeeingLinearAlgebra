# Checkpoint 109 — Gaussian Elimination to Row Echelon Form

## Purpose

Checkpoint 109 combines the elementary row operations from CP107 into a complete Gaussian-elimination sequence.

The lesson begins with

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
2&-1&1&2\\
1&2&-1&2
\end{array}
\right].
\]

It then performs

\[
R_2\leftarrow R_2-2R_1,
\]

\[
R_3\leftarrow R_3-R_1,
\]

\[
R_2\leftrightarrow R_3,
\]

and

\[
R_3\leftarrow R_3+3R_2.
\]

The resulting echelon matrix is

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
0&1&-2&-1\\
0&0&-7&-7
\end{array}
\right].
\]

## Mathematical emphasis

The presentation makes the elimination strategy visible:

1. choose a pivot;
2. create zeros below it;
3. move right to the next pivot column;
4. continue until the pivots form a staircase.

The checkpoint stops at row echelon form. CP110 will use back substitution to solve the resulting triangular system.

## Files

- `engine/gaussian_elimination_to_echelon.py`
- `scenes/gaussian_elimination_to_echelon_presentation.py`
- `tests/test_gaussian_elimination_to_echelon.py`
- `tests/test_gaussian_elimination_to_echelon_presentation.py`
- `scripts/check_cp109_gaussian_elimination_to_echelon.zsh`
- `scripts/render_cp109_gaussian_elimination_to_echelon.zsh`

## Check

```zsh
./scripts/check_cp109_gaussian_elimination_to_echelon.zsh
```

## Render

```zsh
./scripts/render_cp109_gaussian_elimination_to_echelon.zsh
```
