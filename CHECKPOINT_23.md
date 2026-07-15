# Engine v0.3 - Checkpoint 23

## Goal

Extract the proven moving-arrow and coefficient/result-readout coordination from
Checkpoints 21 and 22 into one reusable thin Manim composite adapter:

```text
ManimLinearCombinationPresentation
|- ManimLinearCombinationGeometry
`- ManimLinearCombinationReadout
```

The composite consumes one canonical
`LinearCombinationGeometryDisplaySnapshot` and provides one
`update_from_snapshot(...)` method that updates both established child
adapters from that exact shared state.

## Why this is the correct next step

Checkpoint 21 demonstrated that the moving arrows and numerical readout must be
updated from one shared display snapshot per frame. Checkpoint 22 demonstrated
that this synchronization remains useful when the completed resultant trace is
also present in a lesson-like frame.

The repeated coordination is now established behavior rather than a speculative
abstraction. Extracting it removes scene-level knowledge of how the readout
reaches through a display snapshot to its retained mathematical snapshot.

Checkpoint 23 deliberately does not:

- change any renderer-independent mathematical class;
- change either existing Manim child adapter;
- include the completed trace in the moving composite;
- impose scene layout between arrows and readout;
- refactor a stable smoke scene;
- add a new scene or render script;
- introduce chapter orchestration.

Those concerns remain separate so this checkpoint stays small and coherent.

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
ManimLinearCombinationPresentation
        |-- ManimLinearCombinationGeometry
        `-- ManimLinearCombinationReadout
```

The completed `ManimLinearCombinationTrace` remains an independent immutable
component that a scene may compose beside this moving presentation.

## Added files

```text
CHECKPOINT_23.md
engine/manim_linear_combination_presentation.py
tests/test_manim_linear_combination_presentation.py
scripts/check_manim_linear_combination_presentation.zsh
```

No existing file is modified.

## Public interface

```python
presentation = ManimLinearCombinationPresentation(
    initial_display_snapshot,
    geometry_kwargs={
        "term_arrow_kwargs": {"stroke_width": 6.0},
        "resultant_arrow_kwargs": {"stroke_width": 8.0},
    },
    readout_kwargs={
        "num_decimal_places": 2,
        "include_sign": True,
    },
)

presentation.readout.to_corner(UR)
presentation.update_from_snapshot(later_display_snapshot)
```

The adapter exposes:

```text
mobject
snapshot
geometry
readout
vector_count
display_dimension
coefficient_count
result_dimension
```

## State and layout contract

The composite root is a `VGroup` containing exactly the fixed geometry and
readout adapters. It does not arrange those children relative to one another.
This preserves mathematical display coordinates for the arrows and lets a
scene independently position the readout.

Before either child mutates, every incoming snapshot is validated for:

- canonical display and retained mathematical fields;
- finite projected endpoints;
- finite coefficients and result values;
- term/coefficient agreement;
- unchanged term count;
- unchanged display dimension;
- unchanged coefficient count;
- unchanged result dimension.

After validation, the geometry child receives the complete display snapshot
and the readout receives that same snapshot's exact retained
`linear_combination_snapshot`. Every Manim mobject is updated in place.

## Focused verification

The focused Checkpoint 23 tests cover:

- direct consumption of the actual renderer-independent display snapshot;
- root and child ownership;
- synchronized updates from one snapshot;
- preservation of every arrow, label, matrix, and decimal-entry identity;
- preservation of independently positioned readout entries;
- forwarding and copying of component options;
- higher-dimensional mathematics projected to two dimensions;
- three-dimensional display coordinates;
- canonical-field validation;
- atomic rejection of structural and nonfinite updates.

## Next checkpoint

Checkpoint 24 can refactor the proven Checkpoint 22 smoke scene to use
`ManimLinearCombinationPresentation`. That checkpoint should verify the new
composite with an actual Manim render while leaving the independent completed
trace unchanged.
