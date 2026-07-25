# Checkpoint 71 — From a Line to a Plane to Space

## Goal
Extend the geometric span narrative from CP68–CP70 into three dimensions.

## Mathematical narrative
1. Scalar multiples of one nonzero vector generate a line.
2. Linear combinations of two independent vectors generate a plane.
3. A third vector outside that plane translates the entire plane through space.
4. The span grows only when a generator contributes a genuinely new direction.

## Visual sequence
- Reveal multiples of `u` as a line of endpoints.
- Add `v` and replace the line with a sampled plane and translucent plane patch.
- Pause and predict whether `w` adds a dimension or only another recipe inside the plane.
- Reveal `w` outside the plane.
- Stack translated copies of the `uv`-plane along the `w` direction.
- Add a sparse 3D endpoint field and a gentle ambient camera rotation.
- Reveal `span{u,v,w}=R^3` only after the spatial construction is visible.

## Architecture
- `engine/dimension_growth.py`: renderer-independent ranks, translated planes, and coefficient-generated points.
- `engine/manim_dimension_growth.py`: thin Manim adapter for arrows, planes, and endpoint dots.
- `scenes/dimension_growth_presentation.py`: lesson choreography and presentation.
- focused tests and zsh-compatible test/render scripts.

## Scope
This checkpoint is standalone. It does not modify approved Chapter 1 scenes or the approved CP68–CP70 presentations.
