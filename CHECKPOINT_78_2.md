# Checkpoint 78.2 — Remove Dot Noise and Fix Camera-Oriented Text

## Goal
Simplify CP78 and ensure that all explanatory text remains readable in the 3D scene.

## What changed
- Removed the sampled dot field from the column-space plane because it did not add information to the pivot-column argument.
- Kept the translucent plane as the sole visual representation of the column space.
- Registered the three spatial vector labels as fixed-orientation mobjects so they remain attached to the vector endpoints while always facing the viewer.
- Registered the pivot-column boxes, nonpivot-column box, guide arrows, and explanatory captions as fixed-in-frame overlays so the 3D camera cannot tilt or distort them.

## Visual intention
The viewer should now focus on only three ideas:
- the blue and purple vectors span the plane,
- the yellow vector is redundant,
- pivot positions are found in `R`, but the basis columns come from `A`.

## Files updated
- `scenes/pivot_columns_presentation.py`
- `tests/test_pivot_columns_presentation.py`
- `CHECKPOINT_78_2.md`
