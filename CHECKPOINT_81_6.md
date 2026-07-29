# Checkpoint 81.6 — Prevent the Opening Question from Upscaling

## Problem
The CP81.5 question block was wrapped correctly, but `scale_to_fit_width(...)` enlarged the shorter four-line block until it filled the maximum width. That made the question too large and caused it to interfere with the title.

## Changes
- Preserved the opening title exactly as it was before.
- Reduced the question to a fixed 22-point font size.
- Moved the question slightly lower.
- Changed width handling so the question is scaled only when it is wider than the safe area. It can now be reduced when necessary, but it will never be enlarged.
- Added `scripts/rerender_vector_spaces_opening.zsh`, which rerenders only the opening card and then reassembles the existing chapter video.
- Added the CP81 pacing tests to the chapter check script.

## Files updated
- `scenes/vector_spaces_chapter_cards.py`
- `tests/test_vector_spaces_chapter_pacing.py`
- `scripts/check_vector_spaces_chapter.zsh`
- `scripts/rerender_vector_spaces_opening.zsh`
- `CHECKPOINT_81_6.md`
