# Checkpoint 75 — Inputs That Disappear: The Null Space

## Goal
Introduce the null space as the set of all input vectors sent to the zero vector by a matrix.

## Lesson structure
- Reuse the same rank-2 matrix from CP74.
- Contrast a generic input with the special inputs that map to zero.
- Show the input space on the left and the output space on the right.
- Reveal the line of null inputs in the input space.
- Sweep a moving input along that line while the output remains at the origin.
- Conclude that the null space is a line through the origin.
- Connect the null space to the subspace test and to the rank-nullity theorem.

## Mathematical conclusion
For this matrix,

\[
\operatorname{null}(A)=\operatorname{span}\{\mathbf n\}
\]

and

\[
\dim(\operatorname{null}(A))+\operatorname{rank}(A)=1+2=3.
\]

## Files added
- `engine/null_space.py`
- `scenes/null_space_presentation.py`
- `tests/test_null_space.py`
- `tests/test_null_space_presentation.py`
- `scripts/check_null_space.zsh`
- `scripts/render_null_space.zsh`
- `CHECKPOINT_75.md`
