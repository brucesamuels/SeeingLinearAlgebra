# Checkpoint 71.2 — Missing LEFT Import

## Fix
Added `LEFT` to the Manim imports in `scenes/dimension_growth_presentation.py`.

The prediction animation already used `shift=LEFT * 0.12`; the missing import caused a runtime `NameError` before the third-vector portion of the lesson.

No mathematics, choreography, timing, or approved visual design was changed.
