# Checkpoint 72.6 — Remove the Long Pause and Snap

## Goal
Refine CP72.5 so the two rank collapses begin promptly and animate smoothly, without a long pre-motion delay or an apparent snap at the start of each transition.

## What changed
- Replaced the updater-driven `ValueTracker` transition logic with explicit `UpdateFromAlphaFunc` animations for both collapses.
- This makes the yellow-vector motion and the moving point cloud driven directly by animation alpha on every frame.
- Shortened the pre-motion staging so the first collapse begins sooner.
- Preserved the slow, deliberate overall duration of both collapses.
- Kept the arc-driven renderer-independent mathematics from CP72.5 unchanged.

## Expected effect
The yellow vector should now begin moving much sooner, and both the space-to-plane and plane-to-line collapses should read as continuous motion rather than waiting and snapping.

## Files updated
- `scenes/rank_collapse_3d_presentation.py`
- `tests/test_rank_collapse_3d_presentation.py`
- `CHECKPOINT_72_6.md`
