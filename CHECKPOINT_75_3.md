# Checkpoint 75.3 — Slower Null-Line Reveal and Slower Sweep

## Goal
Refine the null-space lesson so the yellow null points, the yellow null line, and the moving null input all have more time to register visually.

## What changed
- Kept the CP75.2 non-degenerate moving line segment that avoids the origin-crossing crash.
- Separated the null-line reveal into stages:
  1. yellow null points appear first,
  2. then the yellow line is drawn more slowly,
  3. while the points remain visible at reduced opacity.
- Slowed the moving-point sweep along the null line.
- Added slightly longer holds so the viewer can absorb the relation between the sampled points and the full line.

## Visual intention
The viewer should now have more time to see that:
- the yellow sampled points all lie on one line,
- that line is the null space,
- and every moving point on that line still maps to the zero output.

## Files updated
- `scenes/null_space_presentation.py`
- `tests/test_null_space_presentation.py`
- `CHECKPOINT_75_3.md`
