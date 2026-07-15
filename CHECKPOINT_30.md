# Engine v0.3 - Checkpoint 30

## Goal

Close the accumulated linear-combination lesson segment with one concise
post-sweep reflection using the already-proven:

```python
ManimEquationCallout
```

The reflection appears only after the tracker updater has been removed and the
exact endpoint display snapshot has been pinned.

## Why this is the correct next step

Checkpoint 29 completed a coherent instructional progression through:

```text
fixed equation and visual frame
brief Pause and Predict prompt
one-snapshot-per-frame coefficient sweep
exact endpoint pinning
```

The missing lesson beat is a short conceptual conclusion.  Another mathematical
or renderer abstraction is not needed.  The repository already has a reusable
boxed equation callout, and the upper-left region is available again after the
temporary prediction prompt disappears.

Checkpoint 30 therefore reuses the proven callout component rather than adding
a conclusion framework, lesson sequencer, or chapter coordinator.

## Reflection

```text
w is in span{u, v}
Coefficients move the resultant within this span.
```

The displayed TeX source is:

```latex
\mathbf{w}\in\operatorname{span}\left\{\mathbf{u},\mathbf{v}\right\}
```

This statement connects the animated coefficient sweep to the central linear
algebra idea: changing the coefficients changes the particular resultant, but
not the span in which that resultant lies.

## Scene sequencing

The smoke scene now:

1. builds the unchanged renderer-independent coefficient, geometry, display,
   and trace pipeline;
2. reveals the established visual frame and fixed equation callout;
3. presents and removes the existing Pause and Predict prompt;
4. runs the unchanged tracker-driven coefficient sweep;
5. removes the updater and pins the exact final display snapshot;
6. reveals the upper-left span reflection;
7. holds the completed lesson frame briefly for inspection.

## Architectural boundary

The reflection:

- consumes no mathematical or display snapshot;
- performs no vector arithmetic, interpolation, geometry, or projection;
- is not part of the tracker-driven moving group;
- does not alter the fixed equation callout or completed trace;
- is built and sequenced entirely by the scene.

No general lesson or chapter framework is introduced.

## Compatibility

Checkpoint 30 does not change:

```text
engine/scene_tools.py
engine/manim_equation_callout.py
engine/manim_linear_combination_labels.py
engine/manim_linear_combination_presentation.py
engine/manim_linear_combination_trace.py
engine/__init__.py
```

The one-snapshot-per-frame helpers retain their existing signatures and
behavior.  The tracker-driven `VGroup(presentation, labels)` remains intact.

## Files

Intentional replacement:

```text
scenes/linear_combination_presentation_smoke.py
```

Additive files:

```text
CHECKPOINT_30.md
tests/test_linear_combination_post_sweep_reflection_smoke.py
scripts/check_linear_combination_post_sweep_reflection_smoke.zsh
scripts/render_linear_combination_post_sweep_reflection_smoke.zsh
```

## Focused verification

The new tests cover:

- nonempty span-focused reflection wording;
- construction through the proven `ManimEquationCallout` component;
- upper-left placement;
- independence from the moving group, fixed equation callout, and prediction
  prompt;
- preservation of reflection identities and geometry during moving snapshot
  updates;
- consistency of the final mathematical snapshot.

The checkpoint test script also runs all established equation-callout, label,
presentation, and smoke-integration tests before the complete repository suite.

## Render expectation

The approved Checkpoint 29 sequence should remain unchanged through the end of
the coefficient sweep.  After the exact endpoint is pinned, an upper-left boxed
reflection should fade in:

```text
w is in span{u, v}
Coefficients move the resultant within this span.
```

It should remain fixed and should not overlap the title, upper-right readout,
lower-left equation callout, or right-side vector construction.

## Architectural assessment

With the post-sweep reflection, this scene now constitutes the first complete
reusable lesson segment:

```text
orient -> predict -> observe -> reflect
```

It is still not a complete chapter.  A chapter-level composition should wait
until a second lesson segment demonstrates which sequencing and layout patterns
are genuinely repeated.

## Next checkpoint

Checkpoint 31 should preferably begin a second, mathematically distinct lesson
segment using the existing engine architecture.  That second example can reveal
which lesson-level abstractions are truly reusable before any chapter framework
is extracted.
