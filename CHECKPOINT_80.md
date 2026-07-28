# Checkpoint 80 — The Four Fundamental Subspaces

## Goal
Create a Strang-inspired synthesis lesson that organizes the four fundamental subspaces around one master diagram.

## Lesson structure
- Open with the idea that a matrix connects an input space to an output space.
- Build the input-side orthogonal decomposition
  \[
  \mathbb R^n = \operatorname{row}(A) \oplus \operatorname{null}(A).
  \]
- Build the output-side orthogonal decomposition
  \[
  \mathbb R^m = \operatorname{col}(A) \oplus \operatorname{null}(A^T).
  \]
- Show the action of the matrix:
  - the row space is detected by the matrix,
  - the null space is lost to zero,
  - the column space is what the matrix can produce.
- Introduce the left null space as the collection of output directions perpendicular to every possible output.
- Summarize the dimension relationships:
  \[
  \dim(\operatorname{row}(A)) = \dim(\operatorname{col}(A)) = r,
  \]
  \[
  \dim(\operatorname{null}(A)) = n-r,
  \qquad
  \dim(\operatorname{null}(A^T)) = m-r.
  \]
- End with four conceptual descriptions:
  - row space: what the matrix detects,
  - null space: what the matrix loses,
  - column space: what the matrix can produce,
  - left null space: what the matrix cannot reach.

## Visual intention
This lesson is mostly text-led and diagram-led rather than geometry-led. It should feel like a conceptual map of the matrix rather than four separate definitions.

## Files added
- `engine/fundamental_subspaces.py`
- `scenes/fundamental_subspaces_presentation.py`
- `tests/test_fundamental_subspaces.py`
- `tests/test_fundamental_subspaces_presentation.py`
- `scripts/check_fundamental_subspaces.zsh`
- `scripts/render_fundamental_subspaces.zsh`
- `CHECKPOINT_80.md`
