# Checkpoint 79.5 — Add Left and Right Margins to the Bridge Text

## Goal
Fix the “Row reduction tells us...” scrolling text so it no longer stretches too wide across the screen.

## What changed
- Re-broke the bridge text into shorter lines.
- Reduced the font size slightly.
- Preserved the same vertical placement and scrolling motion.
- Kept the theorem layout fix from CP79.4.

## Result
The bridge text should now appear with comfortable left and right margins, consistent with the other text-forward portions of the lesson.

## Files updated
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_5.md`
