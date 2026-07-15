# Engine v0.3 - Checkpoint 20

## Goal

Add the first reusable, snapshot-driven presentation component for the
linear-combination pipeline: a thin Manim readout that displays the current
coefficient vector and resulting vector and updates the same numeric mobjects
in place.

## Why this is the correct next step

Checkpoint 19 completed the mathematical-to-Manim geometry and trace pipeline.
A full instructional chapter also needs explanatory state that remains
synchronized with the animation.

The existing `LinearCombinationSnapshot` already contains the exact
renderer-independent values needed by a coefficient/result readout:

- `coefficients`
- `result`

Checkpoint 20 therefore does not introduce a duplicate mathematical or display
snapshot. It adds only the renderer-specific presentation layer that consumes
those established fields.

## Architectural position

```text
LinearCombination
        |
        v
LinearCombinationSnapshot
        |
        +------------------------------+
        |                              |
        v                              v
existing geometry pipeline     ManimLinearCombinationReadout
```

The new readout is a parallel final adapter. It does not change the geometry,
trace, projection, or Manim arrow adapters.

## Added

- `engine/manim_linear_combination_readout.py`
- `tests/test_manim_linear_combination_readout.py`
- `scripts/check_manim_linear_combination_readout.zsh`
- `CHECKPOINT_20.md`

No existing file is changed.

## New interface

```python
readout = ManimLinearCombinationReadout(snapshot)
readout.update_from_snapshot(later_snapshot)
```

The adapter displays two decimal column vectors:

```text
c = coefficient vector
r = resulting vector
```

The labels are configurable MathTex strings. The numeric entries are fixed
`DecimalNumber` mobjects owned by two `DecimalMatrix` objects.

Public properties include:

- `mobject`
- `snapshot`
- `vector_count`
- `dimension`
- `coefficient_label_mobject`
- `result_label_mobject`
- `coefficient_matrix`
- `result_matrix`
- `coefficient_entries`
- `result_entries`

## Create-once update contract

The coefficient count and result dimension are structural. Every label,
matrix, bracket, and numeric entry is created once in the constructor.

`update_from_snapshot(...)`:

1. validates the complete incoming snapshot;
2. rejects changed coefficient count or result dimension before mutation;
3. updates each existing `DecimalNumber` with `set_value(...)`;
4. preserves the current on-screen center of each numeric entry;
5. retains the exact latest mathematical snapshot.

## Boundaries deliberately preserved

The adapter does not:

- interpolate coefficients;
- scale vectors;
- add vectors;
- construct tip-to-tail geometry;
- project coordinates;
- construct or reveal traces;
- own animation timing;
- recreate numeric mobjects for each frame;
- depend on the older one-off `common` episode components;
- modify any Checkpoint 1-19 implementation.

## Verification

Run the focused tests and complete suite:

```zsh
./scripts/check_manim_linear_combination_readout.zsh
```

Checkpoint 20 adds no scene, so no new render script is appropriate. A focused
readout smoke scene should be a separate checkpoint.
