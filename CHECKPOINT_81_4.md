# Checkpoint 81.4 — Keep the Opening Card Text Inside the Frame

## Goal
Fix the opening card of the assembled Vector Spaces and Subspaces chapter so the title and opening question stay comfortably inside the frame with visible left and right margins.

## Changes
- Wrapped the opening title into three lines instead of two.
- Wrapped the opening question into four shorter lines.
- Added a shared `CARD_TEXT_MAX_WIDTH` limit and applied `scale_to_fit_width(...)` to both the title and question so they remain inside the frame even after font rendering differences.
- Slightly reduced the opening-card font sizes and adjusted the title vertical position.
- Preserved the CP81.3 slowdown and chapter reassembly workflow.

## Files updated
- `scenes/vector_spaces_chapter_cards.py`
- `tests/test_vector_spaces_chapter_pacing.py`
- `CHECKPOINT_81_4.md`
