# Engine v0.3 - Checkpoint 22

## Goal

Add the first complete linear-combination presentation smoke scene by composing
three already-tested visual components:

1. the completed projected resultant trace;
2. the moving tip-to-tail term and resultant arrows;
3. the synchronized coefficient/result readout.

## Why this is the correct next step

Checkpoint 19 verified the completed trace together with moving arrows.
Checkpoint 21 verified moving arrows together with the numerical readout.
Checkpoint 22 now verifies that all three components can occupy one coherent
lesson-like frame while preserving their established state boundaries.

No new mathematical, display, or Manim adapter abstraction is needed.  A
broader presentation-composition class should be based on demonstrated repeated
requirements rather than introduced before this full integration has rendered.

## Architectural position

```text
LinearCombination
        |
CoefficientSweepPath
        |
LinearCombinationGeometry
        |
LinearCombinationGeometryPath
        |
        +-------------------------------+
        |                               |
        v                               v
LinearCombinationTrace       LinearCombinationGeometryDisplayAdapter
        |                               |
LinearCombinationTraceDisplayAdapter   |
        |                               |
ManimLinearCombinationTrace            +-----------------------+
                                        |                       |
                                        v                       v
                         ManimLinearCombinationGeometry  ManimLinearCombinationReadout
                                        |                       |
                                        +-----------+-----------+
                                                    |
                                                    v
                              LinearCombinationPresentationSmoke
```

The trace and moving geometry are projected with the exact same
`LinearDisplayProjector` instance.  Each animation frame asks the display path
for exactly one `LinearCombinationGeometryDisplaySnapshot`; the arrows consume
its display geometry and the readout consumes its retained
`linear_combination_snapshot`.

## Added

- `scenes/linear_combination_presentation_smoke.py`
- `tests/test_linear_combination_presentation_smoke.py`
- `scripts/check_linear_combination_presentation_smoke.zsh`
- `scripts/render_linear_combination_presentation_smoke.zsh`
- `CHECKPOINT_22.md`

No existing file is changed.

## Scene example

The scene preserves the recent two-vector example:

```text
v1 = ( 2, 1)
v2 = (-1, 2)
coefficients: (0, 0) -> (1.25, -0.75)
```

The renderer-independent geometry path is sampled at 33 progress values to
construct one immutable trace.  The scene displays that trace in orange, the
two scaled term arrows in blue and green, the resultant in yellow, and the
coefficient/result readout in the upper-right portion of the frame.

## Shared-frame update

```python
update_linear_combination_presentation(
    animated_mobjects,
    arrows,
    readout,
    display_path,
    progress,
)
```

The helper queries `display_path.snapshot(progress)` exactly once and updates
the existing arrow and decimal mobjects in place.  The fixed trace is not
passed to the helper and is never mutated.

## Boundaries deliberately preserved

Checkpoint 22 does not:

- interpolate coefficients in the scene;
- scale or add vectors in the scene;
- construct tip-to-tail geometry in the scene;
- construct or project trace geometry in Manim;
- query the moving display path more than once per frame;
- recreate arrow, trace, label, bracket, matrix, or decimal mobjects per frame;
- introduce a general chapter coordinator;
- modify Checkpoints 1-21.

## Verification

Run the focused presentation tests and then the complete suite:

```zsh
./scripts/check_linear_combination_presentation_smoke.zsh
```

Render the low-quality preview:

```zsh
./scripts/render_linear_combination_presentation_smoke.zsh
```

The expected render shows the orange resultant trace, moving blue and green
term arrows, moving yellow resultant, and synchronized coefficient/result
readout together in one frame.
