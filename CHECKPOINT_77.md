# Checkpoint 77 — Row Space: What Row Reduction Preserves

## Goal
Show that row reduction changes the actual row vectors, but preserves the row space.

## Lesson structure
- Display a rank-2 matrix and interpret its rows as vectors in \(\mathbb R^3\).
- Reveal the plane spanned by the rows.
- Ask whether row operations change the row space.
- Perform two row operations:
  \[
  R_3\leftarrow R_3-R_1,
  \qquad
  R_3\leftarrow R_3-R_2.
  \]
- Watch the redundant third row collapse away.
- Show the echelon form \(R\).
- Conclude that
  \[
  \operatorname{row}(A)=\operatorname{row}(R).
  \]
- Conclude that the nonzero pivot rows of \(R\) form a basis for the row space.
- State the dimension relation
  \[
  \dim(\operatorname{row}(A))=\operatorname{rank}(A)=2.
  \]

## Files added
- `engine/row_space.py`
- `scenes/row_space_presentation.py`
- `tests/test_row_space.py`
- `tests/test_row_space_presentation.py`
- `scripts/check_row_space.zsh`
- `scripts/render_row_space.zsh`
- `CHECKPOINT_77.md`
