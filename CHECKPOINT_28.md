# Engine v0.3 - Checkpoint 28

## Goal

Integrate the proven `ManimEquationCallout` into the established labeled
linear-combination presentation smoke scene as one fixed scene-level sibling.

The integration remains deliberately narrow:

```text
scene-owned pedagogical sequencing
|
+-- fixed NumberPlane and title
+-- fixed ManimLinearCombinationTrace
+-- fixed ManimEquationCallout
`-- tracker-driven VGroup
    +-- ManimLinearCombinationPresentation
    `-- ManimLinearCombinationLabels
```

## Why this is the correct next step

Checkpoint 27 proved equation and caption construction, panel layout,
validation, and ownership independently.  The smallest useful next step is to
place that component in the already approved lesson frame and let the scene own
when and where it appears.

This integration connects the visual sweep to the concise statement

```text
w = a u + b v
```

without adding chapter orchestration, deriving text from snapshots, or changing
any renderer-independent mathematical class.

## Scene behavior

The smoke scene now:

1. builds the unchanged coefficient, geometry, display, and trace pipeline;
2. constructs the completed resultant trace once;
3. constructs the established moving presentation and labels from one initial
   display snapshot;
4. keeps those moving adapters in the same intact tracker-driven `VGroup`;
5. constructs one fixed `ManimEquationCallout` through
   `build_linear_combination_equation_callout()`;
6. places the callout in the lower-left portion of the frame;
7. reveals the fixed callout before the coefficient sweep;
8. updates only the presentation and labels during the sweep;
9. leaves the callout, title, plane, and completed trace unchanged.

The displayed callout is:

```python
SMOKE_EQUATION = r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}"
SMOKE_EQUATION_CAPTION = "Scale first, then add tip to tail."
```

The equation source is consistent with the existing segment labels:

```text
a u
b v
w
```

## Responsibility boundary

The scene decides:

- callout source text and explanatory caption;
- callout scale, screen position, and appearance timing;
- title, trace, colors, animation duration, and rate function.

`ManimEquationCallout` continues to decide only:

- local equation and caption construction;
- local vertical arrangement;
- surrounding-panel construction;
- component-level validation and ownership.

The renderer-independent pipeline continues to decide:

- coefficient interpolation;
- vector scaling and addition;
- tip-to-tail geometry;
- resultant trace samples;
- display projection.

## Compatibility

Checkpoint 28 does not change:

```text
engine/manim_equation_callout.py
engine/manim_linear_combination_labels.py
engine/manim_linear_combination_presentation.py
engine/manim_linear_combination_trace.py
engine/__init__.py
```

The existing update helpers retain their signatures and behavior.  The callout
is intentionally absent from the one-snapshot-per-frame update path.

## Files

Intentional replacement:

```text
scenes/linear_combination_presentation_smoke.py
```

Additive files:

```text
CHECKPOINT_28.md
tests/test_linear_combination_equation_callout_smoke.py
scripts/check_linear_combination_equation_callout_smoke.zsh
scripts/render_linear_combination_equation_callout_smoke.zsh
```

## Focused verification

The new focused tests cover:

- consistency between the callout equation and the displayed segment labels;
- construction through the proven `ManimEquationCallout` component;
- lower-left scene placement;
- explicit exclusion from the tracker-driven moving group;
- unchanged callout mobject identities and geometry while moving snapshots
  update.

The checkpoint test script also runs the established callout, label,
presentation, and smoke-integration tests before the complete repository suite.

## Render expectation

The approved Checkpoint 26 visual should remain intact.  The render should add a
fixed boxed callout in the lower-left region containing:

```text
w = a u + b v
Scale first, then add tip to tail.
```

The callout should appear before the sweep, remain stationary throughout the
animation, and avoid the moving vectors, upper-right readout, and title.

The render script disables Manim caching so visual approval cannot accidentally
reuse an earlier cached animation segment.

## Next checkpoint

After this integration is visually approved, Checkpoint 29 should add one small
pedagogical beat using an existing scene helper, such as a brief
pause-and-predict moment before the sweep.  It should still avoid a general
chapter framework and should not extract a larger composition until a second
lesson workflow demonstrates repeated stable structure.
