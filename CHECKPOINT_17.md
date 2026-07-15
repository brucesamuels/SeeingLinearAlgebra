# Engine v0.3 — Checkpoint 17

## Linear-combination trace display projection

Checkpoint 17 adds the smallest renderer-independent layer that naturally
follows Checkpoint 16: affine display projection of a completed
`LinearCombinationTrace`.

## Why this is the correct next step

Checkpoint 16 introduced a mathematical trace containing sampled coefficient
vectors, resultant-tip points, and segments joining consecutive tips.  Those
coordinates remain in the original mathematical ambient space.  A renderer
should not decide how an arbitrary-dimensional trace is reduced to 2D or 3D.

`LinearCombinationTraceDisplayAdapter` fills only that projection gap.  It
combines the existing trace object with the already-established
`LinearDisplayProjector`, projects all sampled points and segment endpoints,
and retains the exact mathematical trace snapshot.

No Manim object or smoke scene is added.  A thin Manim trace adapter is a
separate architectural addition for a later checkpoint.

## Architecture

```text
LinearCombination
↓
CoefficientSweepPath
↓
LinearCombinationGeometry
↓
LinearCombinationGeometryPath
↓
LinearCombinationTrace
↓
LinearDisplayProjector
↓
LinearCombinationTraceDisplayAdapter   ← Checkpoint 17
```

The existing instantaneous geometry pipeline remains unchanged and continues
in parallel:

```text
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

## Established conventions followed

Checkpoint 17 uses the actual existing interfaces and patterns:

- `LinearDisplayProjector.project(vectors)`;
- `LinearDisplayProjector.input_dimension`;
- `LinearDisplayProjector.display_dimension`;
- `LinearDisplayProjector.projection_matrix`;
- `LinearDisplayProjector.offset`;
- constructor type and dimension validation;
- immutable, owned display arrays;
- retention of the exact renderer-independent source snapshot; and
- `snapshot()` plus `__call__()` shorthand.

Segment endpoints are flattened before projection because the existing
projector accepts one vector or a row-stored two-dimensional collection.

## Files added

- `engine/linear_combination_trace_display.py`
- `tests/test_linear_combination_trace_display.py`
- `scripts/check_linear_combination_trace_display.zsh`
- `CHECKPOINT_17.md`

No existing file is overwritten.

## New public objects

### `LinearCombinationTraceDisplayAdapter`

Constructed from:

```python
LinearCombinationTraceDisplayAdapter(trace, projector)
```

where `trace` is a `LinearCombinationTrace` and `projector` is the existing
`LinearDisplayProjector`.

Its `snapshot()` method returns a
`LinearCombinationTraceDisplaySnapshot`. Calling the adapter directly is
shorthand for `snapshot()`.

### `LinearCombinationTraceDisplaySnapshot`

Fields:

- `trace_snapshot`
- `display_resultant_points`
- `display_resultant_segments`
- `projection_matrix`
- `display_offset`

Derived properties:

- `coefficients`
- `sample_count`
- `coefficient_dimension`
- `mathematical_dimension`
- `display_dimension`
- `display_resultant_starts`
- `display_resultant_ends`

All newly stored arrays are owned copies and read-only.

## Validation

The adapter rejects:

- a non-`LinearCombinationTrace` source;
- a non-`LinearDisplayProjector` projector; and
- a projector whose input dimension does not equal the mathematical trace
  dimension.

The display snapshot verifies:

- all array ranks and finite values;
- all expected shapes;
- affine projection consistency with the mathematical trace;
- segment starts equal preceding projected points; and
- segment ends equal following projected points.

Single-sample traces retain the stable empty shape
`(0, 2, display_dimension)` for display segments.

## Existing components intentionally unchanged

Checkpoint 17 does not change:

- `LinearCombination`
- `CoefficientSweepPath`
- `LinearCombinationGeometry`
- `LinearCombinationGeometryPath`
- `LinearCombinationTrace`
- `LinearDisplayProjector`
- `LinearCombinationGeometryDisplayAdapter`
- `ManimLinearCombinationGeometry`
- `LinearCombinationGeometrySmoke`
- any rank-collapse component
- `engine/__init__.py`

## Testing

Run:

```zsh
./scripts/check_linear_combination_trace_display.zsh
```

The script adds the repository root to `PYTHONPATH`, runs the focused
Checkpoint 17 tests, and then runs the complete suite.

## Rendering

No render script is added because Checkpoint 17 contains no Manim or renderer
code.  The successful Checkpoint 15 smoke scene remains an optional regression
render.
