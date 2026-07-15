# Engine v0.3 - Checkpoint 24

## Goal

Refactor the complete Checkpoint 22 linear-combination presentation smoke scene
to use the reusable `ManimLinearCombinationPresentation` composite introduced
in Checkpoint 23.

The scene continues to compose two renderer-specific objects with distinct
lifecycles:

```text
ManimLinearCombinationTrace          fixed completed trace
ManimLinearCombinationPresentation   moving arrows + synchronized readout
```

## Why this is the correct next step

Checkpoint 22 proved that the completed trace, moving arrows, and numerical
readout form a useful lesson-like presentation. Checkpoint 23 extracted the
repeated moving-arrow/readout synchronization into one reusable composite.
Checkpoint 24 now verifies that abstraction in its intended scene context and
removes the duplicated child-update logic from the smoke scene.

This checkpoint deliberately does not:

- change renderer-independent mathematics;
- change any display snapshot or projector interface;
- change either child Manim adapter;
- include the immutable trace inside the moving composite;
- add labels, narration, chapter sections, or timing abstractions;
- introduce a general chapter framework.

## Architectural result

```text
LinearCombinationGeometryDisplaySnapshot
                    |
                    v
ManimLinearCombinationPresentation
        |-- ManimLinearCombinationGeometry
        `-- ManimLinearCombinationReadout

LinearCombinationTraceDisplaySnapshot
                    |
                    v
ManimLinearCombinationTrace
```

The scene obtains exactly one moving display snapshot per animation frame and
passes it to `ManimLinearCombinationPresentation.update_from_snapshot(...)`.
The scene no longer knows that the readout consumes the retained mathematical
snapshot inside the display snapshot.

## Files

New files:

```text
CHECKPOINT_24.md
scripts/check_linear_combination_presentation_composite_smoke.zsh
scripts/render_linear_combination_presentation_composite_smoke.zsh
```

Refactored files:

```text
scenes/linear_combination_presentation_smoke.py
tests/test_linear_combination_presentation_smoke.py
```

No engine implementation file is modified.

## Scene contract

The scene:

1. builds the existing renderer-independent coefficient, geometry, display,
   and trace pipeline;
2. constructs the fixed `ManimLinearCombinationTrace` once;
3. constructs one `ManimLinearCombinationPresentation` from the initial display
   snapshot;
4. styles and positions the composite's established child adapters;
5. requests one display snapshot per frame;
6. updates the composite through its single public update method.

All arrows, labels, matrices, brackets, decimal entries, and trace lines retain
their identities throughout the animation.

## Focused verification

The focused tests verify:

- the existing upstream pipeline and shared projector;
- actual renderer-independent trace sampling;
- agreement between trace endpoints and moving display endpoints;
- direct construction of the Checkpoint 23 composite;
- one display-path query per animation frame;
- synchronized geometry and readout state through the composite;
- preservation of all moving mobject identities;
- preservation of all immutable trace line identities and endpoints;
- exact retention of one shared display snapshot at intermediate progress.

## Render expectation

The visual result should match Checkpoint 22:

- orange completed resultant trace;
- blue and green tip-to-tail term arrows;
- yellow resultant arrow;
- synchronized coefficient and result column vectors in the upper-right.

The architectural change should be invisible to the viewer.

## Next checkpoint

Checkpoint 25 can begin the first genuinely reusable lesson-level presentation
component, such as mathematical labels tied to the established vector and
coefficient state. It should remain narrow and should not yet introduce a full
chapter-orchestration framework.
