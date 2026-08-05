# Seeing Linear Algebra — Checkpoint 118

## Topic
Rank, pivots, and consistency.

## Goal
Use the RREF form of an augmented matrix to determine whether a linear system
is consistent and, when it is consistent, whether it has one solution or
infinitely many solutions.

## Central consistency theorem
A system is consistent exactly when adding the right-hand side does not create
an additional pivot:

\[
\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b]).
\]

If

\[
\operatorname{rank}(A)<\operatorname{rank}([A\mid\mathbf b]),
\]

then the augmented matrix contains a contradictory row and the system has no
solution.

## Three model cases

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

Here

\[
\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])=3=n.
\]

Every variable column contains a pivot, so there are no free variables and the
system has one solution.

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

Here

\[
\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])=2<3=n.
\]

The system is consistent, but the nonpivot \(z\)-column produces one free
variable. Therefore the system has infinitely many solutions.

### No solution

\[
\left[
\begin{array}{ccc|c}
1&0&2&4\\
0&1&-1&1\\
0&0&0&3
\end{array}
\right]
\]

The final row says \(0=3\). The augmented column contains an additional pivot,
so

\[
\operatorname{rank}(A)=2<3=\operatorname{rank}([A\mid\mathbf b]).
\]

The system is inconsistent.

## Decision procedure
1. Compare \(\operatorname{rank}(A)\) with
   \(\operatorname{rank}([A\mid\mathbf b])\).
2. If they differ, there is no solution.
3. If they are equal, compare \(\operatorname{rank}(A)\) with the number of
   variables \(n\).
4. Equal to \(n\): unique solution.
5. Less than \(n\): free variables and infinitely many solutions.

For a consistent system,

\[
\#\text{ free variables}=n-\operatorname{rank}(A).
\]

## Pedagogical sequence
1. Count pivots to read rank.
2. Compare a consistent and inconsistent augmented matrix.
3. Pause and predict which system can be solved.
4. Analyze a full-rank unique-solution case.
5. Analyze a rank-deficient consistent case.
6. Analyze an inconsistent augmented-pivot case.
7. Summarize the classification in a decision tree.

## Files
```text
engine/rank_pivots_consistency.py
scenes/rank_pivots_consistency_presentation.py
tests/test_rank_pivots_consistency.py
tests/test_rank_pivots_consistency_presentation.py
scripts/check_cp118_rank_pivots_consistency.zsh
scripts/render_cp118_rank_pivots_consistency.zsh
CHECKPOINT_118.md
```

## Visual review targets
- Scene headings must remain clearly above all bordered content.
- Pivot highlights must identify the intended matrix entries precisely.
- The augmented-column pivot must be visually distinct from coefficient pivots.
- The free-variable column must be clearly marked in the infinite-solution case.
- The final decision tree must remain fully inside the frame without crossed or
  ambiguous arrows.
