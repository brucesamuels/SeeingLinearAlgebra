# Checkpoint 79.8 — Delay the v3 Label Until the Vector Appears

## Goal
Remove the premature appearance of the `v3` label at the start of the graphic sequence.

## Cause
All three vector labels were registered as fixed-orientation objects before the first two vectors were drawn. Registering the third label at that point made it visible before the `v3` arrow appeared.

## Change
- Register only the `v1` and `v2` labels before the first vector animation.
- Register the `v3` label immediately before drawing the `v3` vector.
- Keep the intended simultaneous reveal of the `v3` vector and its label.

## Result
The `v3` label now appears only once, together with the `v3` vector.

## Files updated
- `scenes/rank_nullity_presentation.py`
- `tests/test_rank_nullity_presentation.py`
- `CHECKPOINT_79_8.md`
