# Checkpoint 77.1 — Fix Text Collision in the Row-Space Lesson

## Goal
Remove the text collision late in CP77 when the basis statement, rank statement, and explanatory caption appear together.

## What changed
- Moved the pivot-row basis statement and the dimension statement into a higher text band.
- Kept the explanatory caption in a separate lower band.
- Left the mathematics, choreography, and timing unchanged.
- Added a presentation test to guard against the collision-prone layout.

## Files updated
- `scenes/row_space_presentation.py`
- `tests/test_row_space_presentation.py`
- `CHECKPOINT_77_1.md`
