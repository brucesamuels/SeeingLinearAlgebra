# Engine v0.3 - Checkpoint 29

## Goal

Add one brief pedagogical beat to the established linear-combination lesson frame by using the existing:

```python
engine.scene_tools.pause_and_predict(...)
```

The prompt is a temporary scene-level overlay shown before the coefficient sweep.

## Why this is the correct next step

Checkpoint 28 completed a stable visual frame containing:

```text
fixed plane and title
fixed completed resultant trace
fixed equation callout
tracker-driven presentation and labels
```

The next missing ingredient is not another mathematical or renderer abstraction. It is a small moment in which the viewer is asked to anticipate the tip-to-tail construction before seeing it move.

The repository already provides `pause_and_predict(prompt)`. Checkpoint 29 uses that established helper rather than adding a duplicate component or a general lesson sequencer.

## Prompt

```text
Where should the second scaled vector begin
in a tip-to-tail sum?
```

The question is intentionally structural. The completed orange trace does not answer it; the sweep answers it when the second term segment remains attached to the tip of the first.

## Scene sequencing

The smoke scene now:

1. builds the unchanged renderer-independent coefficient, geometry, display, and trace pipeline;
2. constructs the existing trace, moving presentation, labels, and equation callout;
3. builds a prompt through `pause_and_predict(...)`;
4. places the temporary prompt in the upper-left region;
5. fades the prompt in after the equation callout;
6. pauses briefly for prediction;
7. fades the prompt out completely;
8. starts the unchanged tracker-driven coefficient sweep;
9. pins the exact final display snapshot after removing the updater.

## Architectural boundary

The prompt is not part of:

```text
LinearCombination
CoefficientSweepPath
LinearCombinationGeometry
LinearCombinationGeometryPath
LinearCombinationGeometryDisplayAdapter
ManimLinearCombinationPresentation
ManimLinearCombinationLabels
ManimLinearCombinationTrace
ManimEquationCallout
```

It consumes no snapshots and performs no mathematics, interpolation, geometry, projection, or synchronization.

The scene alone owns:

- prompt wording;
- prompt placement;
- prompt appearance and removal;
- prediction pause duration;
- the decision to place the prompt before the sweep.

## Compatibility

Checkpoint 29 does not change:

```text
engine/scene_tools.py
engine/manim_equation_callout.py
engine/manim_linear_combination_labels.py
engine/manim_linear_combination_presentation.py
engine/manim_linear_combination_trace.py
engine/__init__.py
```

The one-snapshot-per-frame update helpers retain their existing signatures and behavior. The tracker-driven `VGroup(presentation, labels)` remains intact.

## Files

Intentional replacement:

```text
scenes/linear_combination_presentation_smoke.py
```

Additive files:

```text
CHECKPOINT_29.md
tests/test_linear_combination_pause_predict_smoke.py
scripts/check_linear_combination_pause_predict_smoke.zsh
scripts/render_linear_combination_pause_predict_smoke.zsh
```

## Focused verification

The new tests cover:

- nonempty pedagogically relevant prompt text;
- delegation to the existing `pause_and_predict(...)` helper;
- preservation of the helper's two-child heading/question structure;
- upper-left placement;
- explicit exclusion from the tracker-driven moving group;
- independence from the fixed equation callout.

The checkpoint test script also runs the established callout, label, presentation, and smoke-integration tests before the complete repository suite.

## Render expectation

The approved Checkpoint 28 scene should remain intact. Before the coefficient sweep, the render should briefly display an upper-left prompt headed:

```text
Pause and Predict
```

with the question:

```text
Where should the second scaled vector begin
in a tip-to-tail sum?
```

The prompt should disappear before the moving sweep begins. The equation callout, orange trace, labels, readout, and vector motion should remain unchanged.

## Next checkpoint

After this sequencing beat is visually approved, Checkpoint 30 should assess whether the accumulated scene now constitutes a sufficiently complete reusable lesson segment. The next step should preferably add a concise post-sweep reflection or endpoint emphasis, not a general chapter framework. A larger composition should still wait until a second lesson demonstrates repeated structure.


### Typographic refinement

The scalar-vector products use TeX thin spaces, `a\,\mathbf{u}` and
`b\,\mathbf{v}`, in both the moving labels and the fixed equation callout.
This preserves mathematical grouping while preventing the scalar and vector
glyphs from visually crowding one another.

