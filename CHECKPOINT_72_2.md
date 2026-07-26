# Checkpoint 72.2 — Cleaner 3D Rank Collapse Inspired by the Subspaces Applet

## Goal
Refine CP72 so the visuals more clearly communicate the intended sequence:

- rank 3: three vectors generate space,
- rank 2: one vector moves into the plane of the other two,
- rank 1: the generated set contracts cleanly to a line.

## Guidance adopted from the uploaded applet
The matrix tab of the applet makes the target visual logic especially clear:
- a light wireframe cue for full-rank 3D behavior,
- a stable plane state for rank 2,
- a clean line state for rank 1,
- and no leftover surface artifacts in the final line image.

## What changed
- Kept the renderer-independent mathematics unchanged.
- Thinned and faded the parallelepiped edges so they serve only as a volume cue.
- Made the rank-3-to-rank-2 transition read primarily as **one vector moving into the plane** of the other two.
- After reaching rank 2, faded out the wireframe and replaced it with a stable translucent plane patch.
- Removed the old plane-degeneration updater to avoid dragging planar artifacts into the rank-1 state.
- Before the second collapse begins, faded out the plane patch.
- After reaching rank 1, added a clean line cue aligned with the surviving direction.

## Resulting visual logic
1. full-rank vectors and endpoint field occupy space,
2. the third vector becomes coplanar and the endpoint field flattens to a plane,
3. the plane cue disappears before the second collapse,
4. the final line state is rebuilt cleanly.

## Files updated
- `scenes/rank_collapse_3d_presentation.py`
- `tests/test_rank_collapse_3d_presentation.py`
- `CHECKPOINT_72_2.md`

## Notes
This checkpoint is an additive refinement on top of CP72 / CP72.1.
