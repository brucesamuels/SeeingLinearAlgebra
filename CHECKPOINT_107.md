# Seeing Linear Algebra — Checkpoint 107

## Elementary Row Operations

## Goal

Introduce the three legal operations used to transform a linear system without
changing its solution set:

1. interchange two rows;
2. multiply one row by a nonzero scalar;
3. replace one row by itself plus a multiple of another row.

The lesson performs every operation on both the equations and the corresponding
augmented matrix. CP107 introduces the legal moves but does not yet organize
them into the Gaussian-elimination algorithm.

## Mathematical example

The checkpoint uses

\[
\begin{aligned}
x+y&=2,\\
2x-y&=1,
\end{aligned}
\qquad
\left[
\begin{array}{cc|c}
1&1&2\\
2&-1&1
\end{array}
\right],
\]

whose common solution is \((x,y)=(1,1)\).

### Row interchange

\[
R_1\leftrightarrow R_2
\]

produces

\[
\begin{aligned}
2x-y&=1,\\
x+y&=2,
\end{aligned}
\qquad
\left[
\begin{array}{cc|c}
2&-1&1\\
1&1&2
\end{array}
\right].
\]

### Row scaling

\[
R_1\leftarrow 2R_1
\]

produces

\[
\begin{aligned}
2x+2y&=4,\\
2x-y&=1,
\end{aligned}
\qquad
\left[
\begin{array}{cc|c}
2&2&4\\
2&-1&1
\end{array}
\right].
\]

The scalar must be nonzero.

### Row replacement

\[
R_2\leftarrow R_2-2R_1
\]

produces

\[
\begin{aligned}
x+y&=2,\\
-3y&=-3,
\end{aligned}
\qquad
\left[
\begin{array}{cc|c}
1&1&2\\
0&-3&-3
\end{array}
\right].
\]

This last operation previews elimination without yet presenting a general
algorithm.

## Pedagogical sequence

1. Display the equations and augmented matrix side by side.
2. Mark the common solution \((1,1)\).
3. Highlight two rows and interchange them.
4. Restore the original system.
5. Highlight one row and multiply the entire row by 2.
6. Restore the original system.
7. Ask which multiple of row 1 will eliminate the \(x\)-term in row 2.
8. Perform \(R_2\leftarrow R_2-2R_1\) on equations and matrix.
9. Confirm that \((1,1)\) still satisfies the transformed system.
10. Summarize the three general elementary row operations.

## Responsibility boundary

`engine/elementary_row_operations.py` owns:

- augmented-matrix validation;
- row interchange;
- nonzero row scaling;
- row replacement;
- solution verification;
- the CP107 snapshot data.

The Manim scene owns:

- equation and matrix layout;
- row highlighting;
- equation and matrix transformations;
- prediction timing;
- preservation language and final summary.

The engine performs no Manim construction. The scene does not implement
Gaussian elimination, echelon form, or elementary matrices.

## Files

```text
engine/elementary_row_operations.py
scenes/elementary_row_operations_presentation.py
tests/test_elementary_row_operations.py
tests/test_elementary_row_operations_presentation.py
scripts/check_cp107_elementary_row_operations.zsh
scripts/render_cp107_elementary_row_operations.zsh
CHECKPOINT_107.md
```

## Visual review targets

- The two equation rows and two matrix rows align clearly.
- Row highlights make the source and target rows unmistakable.
- The transformed equations and matrix appear simultaneously.
- The operation notation does not collide with the solution badge.
- The prediction question fits comfortably across the frame.
- The row-replacement arithmetic remains legible.
- The final three-operation summary is centered and readable.
- No checkpoint terminology appears in student-facing content.

## Next checkpoint

CP108 should explain why row replacement preserves the solution set, using
reversible equation logic and a geometric interpretation before Gaussian
elimination is introduced.
