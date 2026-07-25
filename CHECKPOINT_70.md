# Checkpoint 70 — When a New Vector Adds Nothing

## Pedagogical goal
Reveal linear dependence as a visible loss of direction before introducing terminology.

## Visual narrative
- Two independent vectors initially generate a plane of endpoints.
- The second generator rotates continuously toward the first.
- A live coefficient field `a u + b v` and its fundamental parallelogram collapse with it.
- A relative-area readout approaches zero.
- Only after the plane has become a line do we reveal `v = c u` and name linear dependence.

## Architecture
- `engine/dependence_collapse.py`: renderer-independent rotation, determinant, rank, parallelogram, and endpoint mathematics.
- `engine/manim_dependence_collapse.py`: identity-preserving thin adapter.
- `scenes/dependence_collapse_presentation.py`: lesson choreography and presentation.
- focused and full-suite zsh scripts.

No approved Chapter 1 or CP68–69 production files are modified.
