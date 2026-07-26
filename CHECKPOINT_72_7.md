# Checkpoint 72.7 — Remove Arrow3D Spinning Artifacts

## Goal
Preserve the smooth arc-driven rank collapse from CP72.6 while removing the visible spinning or twisting artifacts introduced during curved `Arrow3D` motion.

## Cause
`Arrow3D.put_start_and_end_on(...)` repeatedly transforms an existing 3D arrow mesh. During a curved path, the shaft and arrowhead can accumulate visually distracting rotations.

## What changed
- Stored the original keyword arguments for each generator arrow.
- On each frame, rebuilt each `Arrow3D` from the origin to its current endpoint.
- Used `arrow.become(...)` so the arrow slot and surrounding adapter structure remain stable.
- Left the endpoint dots and parallelepiped edges on their existing in-place update paths.
- Did not change the arc mathematics, timings, camera, point cloud, or lesson text.

## Expected effect
The generator vectors should now follow the approved smooth motion without their arrowheads or shafts visibly spinning.

## Files updated
- `engine/manim_rank_collapse_3d.py`
- `tests/test_manim_rank_collapse_3d.py`
- `CHECKPOINT_72_7.md`
