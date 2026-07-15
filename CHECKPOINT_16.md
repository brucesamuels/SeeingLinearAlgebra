# Engine v0.3 — Checkpoint 16

## Linear-combination resultant trace

Checkpoint 16 adds the smallest new renderer-independent capability that
naturally follows the completed Checkpoint 15 pipeline: a finite trace of the
resultant vector across sampled coefficient values.

## Why this is the correct next step

Checkpoint 15 proved that one instantaneous
`LinearCombinationGeometryDisplaySnapshot` can travel through the complete
mathematics-to-display-to-Manim pipeline and update existing arrow mobjects in
place.  The engine still has no renderer-independent object representing the
_history_ or _locus_ of the resultant tip over multiple coefficient samples.

`LinearCombinationTrace` fills only that gap.  It converts a sequence of
existing `LinearCombinationGeometrySnapshot` objects into one immutable trace
snapshot containing:

- coefficient samples;
- resultant-tip points; and
- segments joining consecutive resultant tips.

This provides the mathematical/geometry foundation for a later display adapter
and, separately, a later thin Manim trace renderer.  Those are intentionally
not combined into this checkpoint.

## New architecture

```text
LinearCombination
↓
CoefficientSweepPath
↓
LinearCombinationGeometry
↓
LinearCombinationGeometryPath
├── existing instantaneous display/Manim pipeline
└── LinearCombinationTrace   ← Checkpoint 16
```

## Actual existing interfaces used

The implementation reads only fields already established and verified through
Checkpoint 15:

- `geometry_snapshot.linear_combination_snapshot.coefficients`
- `geometry_snapshot.resultant_segment`

It does not guess or reconstruct constructors for any existing class.

## Files added

- `engine/linear_combination_trace.py`
- `tests/test_linear_combination_trace.py`
- `scripts/check_linear_combination_trace.zsh`
- `CHECKPOINT_16.md`

## Existing files and classes intentionally unchanged

No existing source file is overwritten.  In particular, Checkpoint 16 does not
change:

- `LinearCombination`
- `CoefficientSweepPath`
- `LinearCombinationGeometry`
- `LinearCombinationGeometryPath`
- `LinearDisplayProjector`
- `LinearCombinationGeometryDisplayAdapter`
- `ManimLinearCombinationGeometry`
- `LinearCombinationGeometrySmoke`
- `engine/__init__.py`

The rank-collapse pipeline is also untouched.

## New public objects

### `LinearCombinationTrace`

Constructed from an iterable of existing
`LinearCombinationGeometrySnapshot` objects.  Its `snapshot()` method returns
one immutable `LinearCombinationTraceSnapshot`.

### `LinearCombinationTraceSnapshot`

Fields:

- `coefficients`: shape `(sample_count, coefficient_dimension)`
- `resultant_points`: shape `(sample_count, ambient_dimension)`
- `resultant_segments`: shape
  `(max(sample_count - 1, 0), 2, ambient_dimension)`

Derived properties:

- `sample_count`
- `coefficient_dimension`
- `ambient_dimension`

All arrays are owned copies and are read-only.

## Validation

The trace rejects:

- an empty snapshot sequence;
- missing Checkpoint 15 fields;
- empty or non-vector coefficient samples;
- malformed resultant segments;
- inconsistent coefficient dimensions;
- inconsistent ambient dimensions; and
- nonfinite numerical values.

It supports arbitrary positive ambient dimension.

## Testing

Run:

```zsh
./scripts/check_linear_combination_trace.zsh
```

The script adds the repository root to `PYTHONPATH`, runs the focused
Checkpoint 16 tests, and then runs the complete suite.

## Rendering

No render script is added.  Checkpoint 16 is deliberately renderer-independent
and does not change the successful Checkpoint 15 smoke scene.  A later
checkpoint can add a display projection for the trace, followed by a separate
thin Manim adapter checkpoint.
