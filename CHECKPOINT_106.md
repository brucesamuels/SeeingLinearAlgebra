# Seeing Linear Algebra — Checkpoint 106

## From Equations to an Augmented Matrix

## Goal

Continue the linear-systems chapter by encoding the CP105 system as an
augmented matrix. The lesson explains exactly what is preserved when variable
names and equality signs are suppressed:

- coefficient order;
- one matrix row per equation;
- one coefficient column per variable;
- a final right-hand-side column;
- explicit zero placeholders for missing variables.

CP106 does not yet perform row operations or elimination.

## Mathematical example

The lesson begins with

\[
\begin{aligned}
x+y+z&=3,\\
2x-y+z&=2,\\
x+2y-z&=2.
\end{aligned}
\]

Before suppressing symbols, every coefficient is made explicit:

\[
\begin{aligned}
1x+1y+1z&=3,\\
2x+(-1)y+1z&=2,\\
1x+2y+(-1)z&=2.
\end{aligned}
\]

The augmented matrix is

\[
\left[
\begin{array}{ccc|c}
1&1&1&3\\
2&-1&1&2\\
1&2&-1&2
\end{array}
\right]
=
[A\mid \mathbf b].
\]

A final one-row example emphasizes the zero placeholder:

\[
x-z=4
\quad\longrightarrow\quad
1x+0y+(-1)z=4
\quad\longrightarrow\quad
\begin{bmatrix}1&0&-1&\mid&4\end{bmatrix}.
\]

## Pedagogical sequence

1. Reintroduce the CP105 system.
2. Restore every coefficient, including implied \(1\) and \(-1\).
3. Establish the fixed column order \(x,y,z\mid\mathbf b\).
4. Highlight one equation at a time.
5. Move its three coefficients and constant into one augmented-matrix row.
6. Identify the coefficient block \(A\) and right-hand side \(\mathbf b\).
7. Ask how \(x-z=4\) should be recorded.
8. Reveal the required zero in the \(y\)-column.
9. State the conditions under which the augmented matrix preserves the system.

## Responsibility boundary

`engine/augmented_matrix_encoding.py` owns:

- validation of coefficient matrices, right-hand sides, and variable names;
- construction and splitting of augmented matrices;
- row and variable-column retrieval;
- natural and explicit equation formatting;
- zero-placeholder row encoding.

The Manim scene owns:

- typography and layout;
- equation and matrix construction;
- row-by-row movement of numerical data;
- column color cues;
- block highlighting;
- prediction and conclusion timing.

The engine performs no Manim construction. The scene performs no solving or
row reduction.

## Files

```text
engine/augmented_matrix_encoding.py
scenes/augmented_matrix_encoding_presentation.py
tests/test_augmented_matrix_encoding.py
tests/test_augmented_matrix_encoding_presentation.py
scripts/check_cp106_augmented_matrix_encoding.zsh
scripts/render_cp106_augmented_matrix_encoding.zsh
CHECKPOINT_106.md
```

## Visual review targets

- The natural system remains readable before coefficients are expanded.
- Explicit coefficients align clearly enough to trace into matrix columns.
- Each equation visibly becomes exactly one augmented-matrix row.
- The \(x,y,z,\mathbf b\) headers align with their columns.
- The vertical divider is unmistakable without resembling an extra column.
- The matrix and labels remain comfortably within the frame.
- The zero-placeholder example is readable and not crowded.
- All explanatory text remains on screen long enough to read.
- No checkpoint terminology appears in the student-facing scene.

## Next checkpoint

CP107 should introduce the three elementary row operations and distinguish
legal equation-preserving operations from arbitrary changes to a row.

- The final augmented matrix and zero-placeholder example fade out completely before the conclusion appears.

- The original augmented matrix is fully removed before the missing-variable example appears.
