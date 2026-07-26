# Checkpoint 72.3 — Real-Time Collapse from Space to Plane to Line

## Goal
Refine CP72 so viewers can **watch the generated set collapse in real time**:
- 3D space collapsing into a plane,
- then the plane collapsing into a line.

## What changed
- Kept the renderer-independent rank-collapse mathematics unchanged.
- Kept the thin, faded wireframe volume cue from CP72.2.
- Added a **live plane updater** during the first collapse so the plane patch gradually emerges while the space-filling cloud flattens.
- Kept the endpoint field moving continuously through the entire first collapse.
- Added a **live plane updater and live line updater** during the second collapse.
- During the second collapse, the plane patch narrows and fades while the line cue grows in, so the viewer can watch the plane contract into a line rather than only seeing before-and-after states.
- Preserved the delayed rank language and clean final line state.

## Visual intention
The scene should now communicate:
1. three independent directions generate space,
2. one direction is lost and the whole span collapses into a plane,
3. another direction is lost and the plane collapses into a line.

## Files updated
- `scenes/rank_collapse_3d_presentation.py`
- `tests/test_rank_collapse_3d_presentation.py`
- `CHECKPOINT_72_3.md`

## Notes
This checkpoint is an additive refinement on top of CP72 / 72.1 / 72.2.
