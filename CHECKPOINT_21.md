# Engine v0.3 - Checkpoint 21

## Goal

Add the first focused integration scene for the Checkpoint 20
`ManimLinearCombinationReadout`, synchronizing it with the established moving
linear-combination arrows.

## Why this is the correct next step

Checkpoint 20 created a reusable presentation adapter for the coefficient and
result arrays already present in `LinearCombinationSnapshot`.  Before adding
more presentation components, the engine should verify that the readout and
geometry adapters can be driven together without duplicate path evaluation or
scene-side mathematics.

Checkpoint 21 therefore tests this frame contract:

1. request exactly one `LinearCombinationGeometryDisplaySnapshot`;
2. update `ManimLinearCombinationGeometry` from its projected segment fields;
3. update `ManimLinearCombinationReadout` from its retained
   `linear_combination_snapshot`;
4. preserve all existing Manim mobject identities.

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
LinearCombinationGeometryDisplayAdapter
        |
LinearCombinationGeometryDisplaySnapshot
        |
        +-------------------------------+
        |                               |
        v                               v
ManimLinearCombinationGeometry   ManimLinearCombinationReadout
        |                               |
        +---------------+---------------+
                        |
                        v
          LinearCombinationReadoutSmoke
```

The display snapshot remains the synchronization boundary.  No new
renderer-independent state or coordinator class is introduced.

## Added

- `scenes/linear_combination_readout_smoke.py`
- `tests/test_linear_combination_readout_smoke.py`
- `scripts/check_linear_combination_readout_smoke.zsh`
- `scripts/render_linear_combination_readout_smoke.zsh`
- `CHECKPOINT_21.md`

No existing file is changed.

## Scene example

The scene uses the same small two-vector family used by the recent
linear-combination smoke scenes:

```text
v1 = ( 2, 1)
v2 = (-1, 2)

coefficients:
(0, 0) -> (1.25, -0.75)
```

The two term arrows and the resultant arrow move through the coefficient sweep.
At the same time, fixed decimal column matrices display the current coefficient
vector and resulting vector.

## Shared-frame update helper

```python
update_linear_combination_mobjects(
    animated_mobjects,
    arrows,
    readout,
    display_path,
    progress,
)
```

The helper calls `display_path.snapshot(progress)` exactly once.  It passes that
same display snapshot to the arrow adapter and its exact retained
`linear_combination_snapshot` to the readout adapter.

## Boundaries deliberately preserved

Checkpoint 21 does not:

- introduce another mathematical snapshot;
- interpolate coefficients in the scene;
- calculate scaled terms or resultants in the scene;
- construct or project geometry in Manim;
- add a general chapter coordinator;
- combine the readout with the trace scene;
- modify Checkpoints 1-20;
- recreate arrow, matrix, label, bracket, or decimal-entry mobjects per frame.

A broader presentation composition layer should wait until more than one
focused integration scene establishes the recurring requirements.

## Verification

Run the focused integration tests and then the complete suite:

```zsh
./scripts/check_linear_combination_readout_smoke.zsh
```

Render the low-quality preview:

```zsh
./scripts/render_linear_combination_readout_smoke.zsh
```

The expected render shows a coordinate plane, two tip-to-tail term arrows, a
yellow resultant arrow, and a synchronized coefficient/result readout in the
upper-right portion of the frame.
