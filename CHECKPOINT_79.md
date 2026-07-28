# Checkpoint 79 — Rank and Nullity: Surviving and Disappearing Directions

## Goal
Show how the input dimensions split into directions that survive the transformation and directions that disappear into the null space.

## Lesson structure
- Reuse the same rank-2 matrix from CP77 and CP78.
- Separate the domain into three highlighted input directions:
  - two pivot directions,
  - one null direction.
- Show the two pivot directions mapping to nonzero output vectors.
- Show the null direction mapping to the zero vector.
- Ask where the three input dimensions go.
- Conclude that the input dimensions partition as
  \[
  3 = 2 + 1.
  \]
- State the rank-nullity theorem in this concrete case:
  \[
  \operatorname{rank}(A)+\operatorname{nullity}(A)=3.
  \]

## Visual intention
Students should see that:
- two input directions survive and contribute to the output space,
- one direction disappears completely,
- together they account for all three input dimensions.

## Files added
- `engine/rank_nullity.py`
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity.py`
- `tests/test_rank_nullity_presentation.py`
- `scripts/check_rank_nullity.zsh`
- `scripts/render_rank_nullity.zsh`
- `CHECKPOINT_79.md`
