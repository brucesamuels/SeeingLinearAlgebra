# Engine v0.3 — Checkpoint 15

## Linear-combination geometry smoke scene

Checkpoint 15 adds the first Manim smoke scene for the completed
linear-combination pipeline:

```text
LinearCombination
↓
CoefficientSweepPath
↓
LinearCombinationGeometry
↓
LinearCombinationGeometryPath
↓
LinearDisplayProjector
↓
LinearCombinationGeometryDisplayAdapter
↓
ManimLinearCombinationGeometry
↓
LinearCombinationGeometrySmoke
```

## Architectural purpose

The smoke scene is an integration boundary, not a mathematical layer. It
constructs the existing pipeline, asks the display adapter for snapshots, and
passes each snapshot to the thin Manim adapter.

The scene performs no coefficient interpolation, vector scaling, tip-to-tail
geometry, resultant calculation, or projection.

## Exact Checkpoint 13 display contract

`ManimLinearCombinationGeometry` now consumes the actual Checkpoint 13 fields:

- `display_term_segments`, shape `(term_count, 2, display_dimension)`;
- `display_resultant_segment`, shape `(2, display_dimension)`.

The adapter creates all Manim arrows once and updates those same objects in
place. The earlier endpoint-wrapper fallback remains only for compatibility
with the focused Checkpoint 14 tests.

## Smoke scene

The scene uses

```text
v1 = (2, 1)
v2 = (-1, 2)
```

with coefficients sweeping from `(0, 0)` to `(1.25, -0.75)`. The final
resultant is `(3.25, -0.25)`.

## Verification

```zsh
./scripts/check_linear_combination_geometry_smoke.zsh
./scripts/render_linear_combination_geometry_smoke.zsh
```
