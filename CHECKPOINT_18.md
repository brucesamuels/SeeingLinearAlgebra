# Engine v0.3 - Checkpoint 18

## Goal

Add the first thin Manim adapter for a completed, projected
`LinearCombinationTrace`.

## Architectural position

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
LinearCombinationTraceDisplayAdapter
↓
ManimLinearCombinationTrace
```

## Added

- `engine/manim_linear_combination_trace.py`
- `tests/test_manim_linear_combination_trace.py`
- `scripts/check_manim_linear_combination_trace.zsh`

## Interface

```python
trace_mobject = ManimLinearCombinationTrace(
    display_snapshot,
    segment_kwargs={"stroke_width": 4},
)
```

The adapter consumes only the canonical Checkpoint 17 field:

```python
display_resultant_segments
```

It creates one fixed Manim `Line` per consecutive trace segment and exposes:

- `mobject`
- `snapshot`
- `segment_lines`
- `segment_count`

One-, two-, and three-dimensional display points are converted to Manim's
three-coordinate convention. A single-sample trace produces an empty `VGroup`.

## Boundaries deliberately preserved

This checkpoint does not:

- construct coefficient samples;
- construct mathematical trace geometry;
- project mathematical coordinates;
- update a trace dynamically;
- modify the existing linear-combination arrow adapter;
- add a scene or render script.

A smoke scene combining the moving linear-combination arrows with the completed
trace is reserved for a later checkpoint.

## Verification

Run:

```zsh
./scripts/check_manim_linear_combination_trace.zsh
```

The script adds the repository root to `PYTHONPATH`, runs the focused tests,
and then runs the complete suite.
