# Checkpoint 72.5 — Arc-Driven Real-Time Collapse

## Goal
Refine CP72 so the rank collapse is driven by visibly changing vector directions, especially the yellow vector, while the span points compress with it in real time.

## What changed
- Updated `engine/rank_collapse_3d.py` so the moving generators follow **curved directional interpolation** rather than straight linear blends.
- The first collapse now makes the yellow vector move along a smooth arc into the plane of the other two vectors.
- The second collapse uses the same style of smooth directional motion while the rank-2 plane contracts toward rank 1.
- Preserved continuous point-cloud updates, so the sampled span changes frame by frame with the generators.
- Slowed the scene substantially and removed ambient camera rotation so the changing span, not the camera, carries the lesson.
- Kept the thin, faded wireframe cue for rank 3 and the live plane / line cues for the two collapses.

## Visual intention
Students should now be able to watch:
1. the yellow vector swing into the plane,
2. the 3D point cloud flatten into a plane,
3. the surviving directions continue changing,
4. the plane compress into a line.

## Files updated
- `engine/rank_collapse_3d.py`
- `scenes/rank_collapse_3d_presentation.py`
- `tests/test_rank_collapse_3d.py`
- `tests/test_rank_collapse_3d_presentation.py`
- `CHECKPOINT_72_5.md`
