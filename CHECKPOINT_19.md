# Engine v0.3 - Checkpoint 19

## Goal

Add the first Manim smoke scene for the complete linear-combination resultant
trace pipeline.

## Architectural position

```text
LinearCombination
↓
CoefficientSweepPath
↓
LinearCombinationGeometry
↓
LinearCombinationGeometryPath
├── LinearCombinationGeometryDisplayAdapter
│   ↓
│   ManimLinearCombinationGeometry
│
└── LinearCombinationTrace
    ↓
    LinearCombinationTraceDisplayAdapter
    ↓
    ManimLinearCombinationTrace

                 ↓
LinearCombinationTraceSmoke
```

## Added

- `scenes/linear_combination_trace_smoke.py`
- `tests/test_linear_combination_trace_smoke.py`
- `scripts/check_linear_combination_trace_smoke.zsh`
- `scripts/render_linear_combination_trace_smoke.zsh`

No existing engine, display, adapter, or scene file is changed.

## Scene behavior

The scene uses the established two-vector example

```text
v1 = (2, 1)
v2 = (-1, 2)
```

with coefficients sweeping from `(0, 0)` to `(1.25, -0.75)`.

The geometry path is sampled at 33 progress values. Those actual
`LinearCombinationGeometrySnapshot` objects are supplied to
`LinearCombinationTrace`; the trace is projected with the same
`LinearDisplayProjector` instance used by the moving arrow display path.

The completed trace is rendered as fixed Manim lines. The existing term and
resultant arrow mobjects are then updated in place as progress runs from zero
to one.

## Boundaries deliberately preserved

The scene does not:

- interpolate coefficients itself;
- scale or add vectors itself;
- construct tip-to-tail geometry itself;
- construct trace segments itself;
- project coordinates itself;
- recreate moving arrows on each frame;
- introduce a dynamic-trace adapter;
- modify any stable Checkpoint 1-18 implementation.

## Verification

Run the focused tests and complete suite:

```zsh
./scripts/check_linear_combination_trace_smoke.zsh
```

Render the smoke scene:

```zsh
./scripts/render_linear_combination_trace_smoke.zsh
```
