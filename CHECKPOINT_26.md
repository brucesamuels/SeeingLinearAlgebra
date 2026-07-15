# Engine v0.3 - Checkpoint 26

## Goal

Integrate the proven `ManimLinearCombinationLabels` adapter into the existing
linear-combination presentation smoke workflow without changing the stable
renderer-independent pipeline or the established
`ManimLinearCombinationPresentation` composite.

The labels remain a scene-level sibling of the moving presentation:

```text
LinearCombinationGeometryDisplaySnapshot
|
+---> ManimLinearCombinationPresentation
|     |-- ManimLinearCombinationGeometry
|     `-- ManimLinearCombinationReadout
|
`---> ManimLinearCombinationLabels

LinearCombinationTraceDisplaySnapshot
|
`---> ManimLinearCombinationTrace
```

Each animation frame obtains exactly one display snapshot.  That exact object
is passed to both moving adapters.

## Why this is the correct next step

Checkpoint 25 proved label construction, validation, midpoint anchoring, and
identity-preserving updates independently.  The smallest useful next step is
to demonstrate those labels in the already established lesson-like scene.

This checkpoint intentionally does not add a new lesson or chapter framework.
It also does not expand `ManimLinearCombinationPresentation`.  Keeping labels
as a sibling lets the scene decide when they appear while preserving the
existing composite's narrow responsibility for synchronized arrows and
numerical readout.

## Scene behavior

The smoke scene now:

1. builds the unchanged renderer-independent coefficient, geometry, display,
   and trace pipeline;
2. constructs the completed resultant trace once;
3. constructs the established moving presentation composite once;
4. constructs `ManimLinearCombinationLabels` from the same initial display
   snapshot;
5. colors the term labels to match their arrows and colors the resultant label
   to match the resultant arrow;
6. keeps the presentation and labels in one intact scene-level moving group;
7. reveals that synchronized group with one `FadeIn`;
8. requests one display snapshot per animation frame;
9. passes that exact snapshot to the presentation and labels;
10. preserves every existing arrow, readout, label, and trace-line identity.

The smoke labels are:

```text
a u
b v
w
```

with TeX sources:

```python
(r"a\mathbf{u}", r"b\mathbf{v}")
r"\mathbf{w}"
```

## Responsibility boundary

The scene decides:

- when the trace, presentation, and labels appear;
- colors, font size, and scene-specific per-term label offsets;
- animation duration and rate function.

The scene does not compute:

- coefficients;
- vector sums;
- tip-to-tail segments;
- interpolation;
- projection;
- trace samples;
- label midpoint anchors.

## Compatibility

The existing `update_linear_combination_presentation(...)` helper remains
unchanged so Checkpoint 24 tests and callers continue to work.

Checkpoint 26 adds a separate helper:

```python
update_labeled_linear_combination_presentation(
    presentation,
    labels,
    display_path,
    progress,
)
```

It performs one display-path lookup and forwards the same snapshot object to
both established adapters.

## Files

Refined files:

```text
engine/manim_linear_combination_labels.py
scenes/linear_combination_presentation_smoke.py
tests/test_manim_linear_combination_labels.py
```

Additive files:

```text
CHECKPOINT_26.md
tests/test_linear_combination_labeled_presentation_smoke.py
scripts/check_linear_combination_labeled_presentation_smoke.zsh
scripts/render_linear_combination_labeled_presentation_smoke.zsh
```

The label adapter gains an optional, backward-compatible
`term_label_offsets` sequence.  Existing callers that provide only
`term_label_offset` retain the original shared-offset behavior.  This
checkpoint still does not modify:

```text
engine/__init__.py
engine/manim_linear_combination_presentation.py
engine/manim_linear_combination_geometry.py
engine/manim_linear_combination_readout.py
engine/manim_linear_combination_trace.py
```

## Focused verification

The new focused tests cover:

- the scene remains a real Manim `Scene`;
- label configuration agrees with the smoke vector count;
- presentation and labels consume the same initial display snapshot;
- the per-frame helper queries the display path exactly once;
- the exact returned snapshot is forwarded to both adapters;
- geometry, readout, and label positions remain synchronized;
- all moving mobject identities are preserved;
- completed trace mobjects remain unchanged.

The checkpoint test script also runs the existing label, presentation, and
presentation-smoke tests before running the complete repository suite.

## Render expectation

The rendered scene should preserve the established visual result and add:

- a blue `a\mathbf{u}` label near the first term segment;
- a green `b\mathbf{v}` label near the second term segment;
- a yellow `\mathbf{w}` label near the resultant segment.

The labels should move with their corresponding displayed segments throughout
the coefficient sweep.  The first term label is offset above-left and the
second term label above-right so each remains visually separated from its
segment.  These distinct offsets also avoid a complete overlap at the exact
zero-vector starting state.

## Next checkpoint

After the labeled smoke scene is visually approved, Checkpoint 27 should add
one small reusable explanatory-text or equation-callout component, or extract a
labeled composite only if the scene integration demonstrates stable repeated
coordination.  It should not yet introduce general chapter orchestration.
