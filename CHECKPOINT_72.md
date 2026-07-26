# Checkpoint 72 — Three Vectors, But How Many Directions?

## Goal
Synthesize the geometric ideas of span, dependence, dimension, and rank in one continuous 3D lesson.

## Mathematical narrative
Three vectors in `R^3` do not necessarily provide three independent directions.

1. **Rank 3:** three independent generators produce a spatial endpoint field and a nonzero-volume parallelepiped.
2. **Rank 2:** the third generator moves continuously into the span of the first two; volume collapses to zero and every endpoint lies in a plane.
3. **Rank 1:** the remaining generators align; the plane and endpoint field collapse onto a line.

The word **rank** is attached to each state only after its geometry is visible.

## Architecture
- `engine/rank_collapse_3d.py` contains all generator interpolation, endpoint sampling, determinant, rank, and parallelepiped mathematics.
- `engine/manim_rank_collapse_3d.py` is a thin identity-preserving adapter.
- `scenes/rank_collapse_3d_presentation.py` owns choreography, camera motion, prompts, and delayed terminology.

## Visual design
- A moderate endpoint field makes the span visible without excessive render cost.
- A parallelepiped provides a volume cue during rank 3.
- A translucent plane appears at rank 2 and then contracts during the rank-2-to-rank-1 transition.
- Ambient camera rotation supports depth perception.
- Fixed-in-frame text remains readable throughout.

## Acceptance question
Does the scene make it visually convincing that three vectors may generate space, a plane, or a line depending on how many independent directions remain?
