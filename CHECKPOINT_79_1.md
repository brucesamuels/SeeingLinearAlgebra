# Checkpoint 79.1 — Every Input Splits: Row Space Plus Null Space

## Goal
Replace the original CP79 concept with a stronger visualization of rank-nullity.

Instead of repeating the null-space idea, this lesson shows that every input vector splits uniquely into:
- a component in the row space, and
- a component in the null space.

## Core mathematical idea
For the input vector \(\mathbf x\),
\[
\mathbf x = \mathbf x_{\mathrm{row}} + \mathbf x_{\mathrm{null}}.
\]

Then the matrix acts by
\[
A\mathbf x = A\mathbf x_{\mathrm{row}} + A\mathbf x_{\mathrm{null}} = A\mathbf x_{\mathrm{row}} + \mathbf 0.
\]

So the null component disappears, while the row-space component completely determines the output.

## Visual structure
- Draw the input space on the left and the output space on the right.
- In the input space, show:
  - the row-space plane,
  - the null-space line,
  - one generic input vector \(\mathbf x\).
- Decompose \(\mathbf x\) into \(\mathbf x_{\mathrm{row}}\) and \(\mathbf x_{\mathrm{null}}\).
- Show that only \(\mathbf x_{\mathrm{row}}\) contributes to the output.
- Conclude with the domain decomposition
  \[
  \mathbb R^3 = \operatorname{row}(A) \oplus \operatorname{null}(A),
  \]
  and the dimension count
  \[
  \dim(\operatorname{row}(A)) + \dim(\operatorname{null}(A)) = 2 + 1 = 3.
  \]

## Why this is better
This version distinguishes CP79 from the earlier null-space lesson by showing how **every input vector** participates in the rank-nullity theorem, not just the special vectors in the null space.

## Files updated
- `engine/rank_nullity.py`
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_1.md`
