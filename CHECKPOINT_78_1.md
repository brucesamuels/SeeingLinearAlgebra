# Checkpoint 78.1 — Improve CP78 Readability and Clarify the Highlights

## Goal
Refine CP78 so the vector labels are easier to read, the three vectors are more clearly distinguished in space, the matrices visually match the 3D vectors, and the pivot/nonpivot highlighting is more self-explanatory.

## What changed
- Rotated the 3D view to better separate the three column vectors.
- Increased the vector-label size and added a dark background stroke so the labels remain readable over the scene.
- Color-coded the columns of both `A` and `R` to match the vector colors in the 3D diagram.
- Replaced the generic green pivot highlight with column-colored pivot boxes and guides.
- Added short captions so the highlight stage explicitly explains what is being shown:
  - `Pivot columns in R`
  - `The third column is nonpivot, so it is redundant.`

## Visual intention
The lesson should now make it clearer that:
- blue and purple are the pivot columns,
- the yellow column is the nonpivot column,
- pivot positions are found in `R`,
- but the basis vectors themselves come from the original matrix `A`.

## Files updated
- `scenes/pivot_columns_presentation.py`
- `tests/test_pivot_columns_presentation.py`
- `CHECKPOINT_78_1.md`
