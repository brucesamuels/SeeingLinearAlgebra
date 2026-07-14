# Engine v0.3 - Checkpoint 13

## Architectural goal

Add a renderer-independent display adapter for coefficient-sweep geometry:

```text
LinearCombinationGeometryPath
            |
            v
LinearDisplayProjector
            |
            v
LinearCombinationGeometryDisplayAdapter
            |
            v
LinearCombinationGeometryDisplaySnapshot
```

The adapter projects every mathematical segment endpoint into a chosen display
space while preserving the term ordering, tip-to-tail adjacency, and the
resultant's shared origin and final tip.

## Why this belongs in the engine

The choice of how an `R^n` mathematical state is shown in `R`, `R^2`, or `R^3`
is a display concern, but it is still renderer independent.  Manim should
receive display-ready numerical arrays rather than own projection matrices or
reshape mathematical data.

Keeping this layer in the engine allows future renderers to consume exactly the
same projected geometry.

## Existing classes left unchanged

Checkpoint 13 does not modify:

- `LinearCombination`
- `LinearCombinationSnapshot`
- `CoefficientSweepPath`
- `LinearCombinationGeometry`
- `LinearCombinationGeometrySnapshot`
- `LinearCombinationGeometryPath`
- `LinearDisplayProjector`
- the complete rank-collapse pipeline
- any Manim adapter or scene

Only `engine/__init__.py` receives a public export line during installation.

## New public classes

### `LinearCombinationGeometryDisplayAdapter`

The adapter owns an existing `LinearCombinationGeometryPath` and an existing
`LinearDisplayProjector`.

For each progress value it:

1. requests one renderer-independent geometry snapshot from the path;
2. flattens the term endpoints into a row-stored point collection;
3. projects those endpoints with `LinearDisplayProjector.project`;
4. restores the shape `(vector_count, 2, display_dimension)`;
5. projects the two resultant endpoints;
6. returns a validated display snapshot.

It does not interpolate coefficients, reconstruct partial sums, or duplicate
segment geometry.

### `LinearCombinationGeometryDisplaySnapshot`

The snapshot retains:

- the complete original `LinearCombinationGeometrySnapshot`;
- projected tip-to-tail term segments;
- the projected resultant segment;
- the projection matrix;
- the display offset.

All public numerical arrays are owned, finite, and read only.

## Affine projection

`LinearDisplayProjector` uses

```text
x -> P x + b
```

so the offset is applied to every endpoint.  Shared mathematical endpoints are
therefore still shared in display space, and the projected term chain remains
tip to tail.

## Deliberate exclusions

Checkpoint 13 adds no:

- Manim imports;
- arrow mobjects;
- colors or styling;
- animation timing or easing;
- smoke scene.

These remain responsibilities of later thin adapters and scenes.

## Files added

```text
engine/linear_combination_geometry_display.py
tests/test_linear_combination_geometry_display.py
scripts/check_linear_combination_geometry_display.zsh
CHECKPOINT_13.md
```

## Testing

The focused tests cover:

- identity projection;
- high-dimensional axis selection;
- affine offsets;
- nontrivial projection matrices;
- preservation of endpoint order and tip-to-tail topology;
- retention of the mathematical snapshot;
- dimensional validation;
- immutable arrays;
- exact delegation boundaries;
- sampled snapshot sequences;
- progress-validation ownership;
- call shorthand.

## Next checkpoint

Checkpoint 14 should add a thin Manim adapter that consumes
`LinearCombinationGeometryDisplaySnapshot`, creates arrow mobjects once, and
updates those same objects without performing mathematics or projection.
