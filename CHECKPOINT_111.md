# Seeing Linear Algebra — Checkpoint 111

## Topic
The Gaussian elimination algorithm as a reusable pivot cycle.

## Goal
Generalize the worked elimination example into a repeatable procedure:

1. Find a nonzero pivot.
2. Swap it into the pivot position if needed.
3. Clear every entry below it.
4. Move one row down and one column right.
5. Repeat until no pivot remains.

## Demonstration matrix

\[
\left[
\begin{array}{ccc|c}
0&1&1&2\\
1&1&1&3\\
2&3&1&6
\end{array}
\right].
\]

The zero in the first pivot position forces a row search and swap:

\[
R_1\leftrightarrow R_2.
\]

Then clear below the first pivot:

\[
R_3\leftarrow R_3-2R_1.
\]

Move to the smaller active submatrix and clear below the second pivot:

\[
R_3\leftarrow R_3-R_2.
\]

The echelon form is

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
0&1&1&2\\
0&0&-2&-2
\end{array}
\right].
\]

## Visual structure
- A persistent pivot-cycle checklist appears at the right.
- The current checklist step is yellow; completed steps become green.
- A blue rectangle marks the active submatrix.
- The active region shrinks after each pivot column is completed.
- Pivot entries are highlighted in blue, green, and red.
- The final screen pairs the echelon matrix with the completed algorithm.

## Files
```text
engine/elimination_algorithm.py
scenes/elimination_algorithm_presentation.py
tests/test_elimination_algorithm.py
tests/test_elimination_algorithm_presentation.py
scripts/check_cp111_elimination_algorithm.zsh
scripts/render_cp111_elimination_algorithm.zsh
CHECKPOINT_111.md
```


## Revision 1 — collision correction
- Moved row-operation formulas above the matrix on the left.
- Moved the “No row swap is needed” note into the same dedicated operation band.
- Kept all transient operation text clear of the persistent Pivot cycle panel.
- Added a presentation-source regression test for the operation anchor.
