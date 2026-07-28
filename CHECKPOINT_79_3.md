# Checkpoint 79.3 — Text-Led Rank–Nullity Synthesis

## Goal
Replace the geometry-heavy CP79 approach with a largely textual synthesis lesson.

## Structure
1. Slow scrolling text explains that a dependent vector adds no new direction and therefore no new dimension.
2. A brief 3D callback shows two independent vectors and a third vector moving into their plane, where it becomes dependent.
3. Slow scrolling text recalls that row reduction identifies pivot positions.
4. A brief matrix callback shows that pivot positions are found in `R`, while the corresponding original columns of `A` form a basis for the column space.
5. Slow scrolling text explains that the remaining input directions appear in the null space and collapse to the zero vector.
6. The lesson concludes with the rank–nullity theorem:
   \[
   \operatorname{rank}(A)+\operatorname{nullity}(A)=n.
   \]

## Final interpretation
- Rank counts the independent directions that survive.
- Nullity counts the directions that collapse to zero.
- Together, they account for the entire input space.

## Files updated
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_3.md`
