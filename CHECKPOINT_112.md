# Seeing Linear Algebra — Checkpoint 112

## Topic
Gauss–Jordan elimination and reduced row echelon form.

## Goal
Start from row echelon form and continue eliminating until each pivot equals 1
and every pivot column is otherwise zero. The lesson should end by showing that
RREF allows the solution to be read directly, and compare this with the back
substitution route from CP110.

## Mathematical content
Begin with the echelon matrix from the previous lessons:

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
0&1&-2&-1\\
0&0&-7&-7
\end{array}
\right].
\]

Apply the row operations

\[
R_3\leftarrow -\frac{1}{7}R_3,
\qquad
R_2\leftarrow R_2+2R_3,
\qquad
R_1\leftarrow R_1-R_3,
\qquad
R_1\leftarrow R_1-R_2.
\]

This produces the reduced row echelon form

\[
\left[
\begin{array}{ccc|c}
1&0&0&1\\
0&1&0&1\\
0&0&1&1
\end{array}
\right],
\]

so the solution is read directly as

\[
x=1,\qquad y=1,\qquad z=1.
\]

## Pedagogical sequence
1. Reintroduce the row echelon matrix.
2. State the goals of reduced row echelon form.
3. Scale the bottom pivot to 1.
4. Clear the entries above the bottom pivot.
5. Clear the entry above the middle pivot.
6. Read the solution directly from the final matrix.
7. Compare this method to back substitution.

## Files
```text
engine/gauss_jordan_rref.py
scenes/gauss_jordan_rref_presentation.py
tests/test_gauss_jordan_rref.py
tests/test_gauss_jordan_rref_presentation.py
scripts/check_cp112_gauss_jordan_rref.zsh
scripts/render_cp112_gauss_jordan_rref.zsh
CHECKPOINT_112.md
```

## Visual review targets
- Operation labels stay above the matrix on the left and never collide with the right-side goals panel.
- The right-side panel remains unobstructed throughout the lesson.
- Focus rectangles clearly indicate the active row and pivot column at each step.
- The direct read-off panel is visually distinct from the earlier goals panel.
- The final comparison screen is balanced and easy to read.
