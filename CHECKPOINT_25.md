# Engine v0.3 - Checkpoint 25

## Goal

Add the first narrow reusable lesson-level semantic component:

```text
ManimLinearCombinationLabels
```

The adapter owns fixed mathematical labels for the displayed linear-combination
term segments and resultant segment. It consumes one already projected
`LinearCombinationGeometryDisplaySnapshot`, anchors each label at the midpoint
of its corresponding segment plus a configurable display-space offset, and
moves the existing labels in place when a compatible later snapshot arrives.

## Why this is the correct next step

Checkpoint 24 completed a stable lesson-like visual core:

```text
ManimLinearCombinationTrace           fixed completed trace
ManimLinearCombinationPresentation    moving arrows + synchronized readout
```

The first complete chapter will also need semantic cues that connect the moving
geometry to mathematical language. Labels are the smallest such cue. Their
behavior is now sufficiently well bounded to isolate without inventing chapter
orchestration:

- label text is fixed lesson configuration;
- label position is derived only from already projected display geometry;
- term count and display dimension are structural;
- labels can update from the same display snapshot already used by the moving
  presentation;
- scene timing and pedagogical sequencing remain outside the adapter.

This checkpoint intentionally proves the component independently before adding
it to `ManimLinearCombinationPresentation` or a smoke scene. That preserves the
project's established pattern: demonstrate one stable responsibility, test it,
then integrate it in a later checkpoint.

## Architectural position

```text
LinearCombinationGeometryDisplaySnapshot
                    |
          +---------+------------------------+
          |                                  |
          v                                  v
ManimLinearCombinationPresentation   ManimLinearCombinationLabels
          |-- ManimLinearCombinationGeometry
          `-- ManimLinearCombinationReadout
```

`ManimLinearCombinationLabels` is an independent sibling of the existing
moving presentation composite in Checkpoint 25. No existing composite is
expanded yet.

## Public interface

```python
labels = ManimLinearCombinationLabels(
    initial_display_snapshot,
    term_labels=(r"a\mathbf{u}", r"b\mathbf{v}"),
    resultant_label=r"\mathbf{r}",
    term_label_offset=(0.0, 0.25),
    resultant_label_offset=(0.0, -0.25),
    label_kwargs={"font_size": 32},
)

labels.update_from_snapshot(later_display_snapshot)
```

When `term_labels` is omitted, the adapter generates term labels in order:

```text
c_1 v_1, c_2 v_2, ..., c_k v_k
```

The adapter exposes:

```text
mobject
snapshot
term_label_mobjects
resultant_label_mobject
term_label_sources
resultant_label_source
term_count
display_dimension
term_label_offset
resultant_label_offset
update_from_snapshot(...)
```

## State and validation contract

The root object is a `VGroup` containing exactly the fixed term-label `MathTex`
mobjects followed by the fixed resultant-label `MathTex` mobject.

Before construction or update, the adapter validates:

- canonical `display_term_segments` and `display_resultant_segment` fields;
- term-segment shape `(term_count, 2, display_dimension)`;
- resultant-segment shape `(2, display_dimension)`;
- at least one term;
- display dimension equal to 2 or 3;
- finite projected coordinates;
- label-source count and nonempty string content;
- finite two- or three-dimensional label offsets;
- mapping-based `MathTex` options.

Before any label moves during an update, the complete incoming snapshot is
validated and checked for unchanged term count and display dimension. Every
label mobject retains its identity.

## Responsibility boundary

The adapter does:

- own fixed `MathTex` labels;
- retain immutable label sources and offsets;
- calculate display-space midpoint anchors from projected segments;
- move labels in place after complete structural validation.

The adapter does not:

- compute coefficients or vector sums;
- interpolate coefficient paths;
- construct tip-to-tail geometry;
- project mathematical coordinates;
- modify arrow, trace, or readout adapters;
- decide when labels appear or disappear;
- arrange chapter sections, narration, or animation timing.

## Files

All files are additive:

```text
CHECKPOINT_25.md
engine/manim_linear_combination_labels.py
tests/test_manim_linear_combination_labels.py
scripts/check_manim_linear_combination_labels.zsh
```

No existing file is modified. In particular, this checkpoint does not modify:

```text
engine/__init__.py
engine/manim_linear_combination_presentation.py
engine/manim_linear_combination_geometry.py
engine/manim_linear_combination_readout.py
engine/manim_linear_combination_trace.py
scenes/linear_combination_presentation_smoke.py
```

## Focused verification

The focused tests cover:

- direct consumption of an actual renderer-independent display snapshot;
- midpoint anchoring with the default offsets;
- root and child ownership;
- generated and custom TeX sources;
- copied and observable `MathTex` options;
- two- and three-dimensional display coordinates;
- in-place updates with exact snapshot retention;
- preservation of every label identity;
- canonical-field, shape, finite-value, label, offset, and option validation;
- atomic rejection of incompatible term counts, display dimensions, and
  nonfinite updates.

The checkpoint test script adds the repository root to `PYTHONPATH`, runs the
focused test file, and then runs the complete repository test suite.

## Render decision

Checkpoint 25 adds no scene and changes no scene. Therefore it adds no render
script. A real Manim render becomes appropriate when the labels are integrated
into a focused presentation scene in a later checkpoint.

## Next checkpoint

Checkpoint 26 can integrate the proven labels into the existing
linear-combination presentation workflow, preferably through one narrowly
scoped scene or composite change. That checkpoint should preserve one display
snapshot per frame and should decide label appearance through scene-level
pedagogical sequencing rather than embedding timing in the adapter.
