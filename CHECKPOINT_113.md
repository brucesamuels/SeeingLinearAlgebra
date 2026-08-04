# Seeing Linear Algebra — Checkpoint 113

## Topic
Reading the solution-set type directly from reduced row echelon form.

## Goal
Use three comparable three-variable RREF examples to distinguish the three
possible outcomes for a linear system:

1. a unique solution,
2. no solution,
3. infinitely many solutions.

## Mathematical examples

### Unique solution

\[
\left[
\begin{array}{ccc|c}
1&0&0&2\\
0&1&0&-1\\
0&0&1&3
\end{array}
\right]
\]

gives

\[
x=2,\qquad y=-1,\qquad z=3.
\]

Every variable column contains a pivot.

### No solution

\[
\left[
\begin{array}{ccc|c}
1&0&2&4\\
0&1&-1&1\\
0&0&0&1
\end{array}
\right]
\]

contains the contradictory equation

\[
0=1.
\]

Therefore the system is inconsistent.

### Infinitely many solutions

\[
\left[
\begin{array}{ccc|c}
1&0&2&4\\
0&1&-1&1\\
0&0&0&0
\end{array}
\right]
\]

has no contradiction, but the \(z\)-column is not a pivot column. Letting
\(z=t\) gives

\[
x=4-2t,\qquad y=1+t,\qquad z=t.
\]

One free parameter generates infinitely many solutions.

## Pedagogical sequence
1. Read a unique solution directly from RREF.
2. Pause before interpreting the last row of an inconsistent matrix.
3. Connect \([0\ 0\ 0\mid1]\) to the impossible equation \(0=1\).
4. Replace the contradiction by a zero row.
5. Identify the non-pivot \(z\)-column as free.
6. Introduce a parameter and display the resulting family of solutions.
7. End with a three-card recognition summary.

## Files
```text
engine/rref_solution_sets.py
scenes/rref_solution_sets_presentation.py
tests/test_rref_solution_sets.py
tests/test_rref_solution_sets_presentation.py
scripts/check_cp113_rref_solution_sets.zsh
scripts/render_cp113_rref_solution_sets.zsh
CHECKPOINT_113.md
```

## Visual review targets
- The left matrix and right interpretation panel remain separated.
- The contradictory row is unmistakably highlighted.
- The free-variable column and zero row use distinct highlights.
- The parameter equations fit comfortably in the right panel.
- The final three summary cards remain inside the frame and do not overlap.
