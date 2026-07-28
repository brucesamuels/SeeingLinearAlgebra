# Checkpoint 79.7 — Correct Final Reveal Order

## Goal
Prevent the final explanatory text from appearing prematurely, disappearing, and then reappearing.

## Cause
The interpretation block was registered as a fixed-in-frame object at the same time as the theorem and example. In Manim, that registration made it visible before its intended `FadeIn`.

## Fix
- Register only the title line, theorem, and example for the first reveal.
- Pause briefly.
- Register the interpretation block only immediately before its own fade-in.

## Result
The final screen now reveals in the intended order:
1. title line,
2. theorem equation and `2+1=3`,
3. explanatory text.

## Files updated
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_7.md`
