# Engine v0.3 - Checkpoint 27

## Goal

Add one narrow reusable lesson-level explanatory component:

```text
ManimEquationCallout
```

The component owns one fixed boxed `MathTex` equation and an optional fixed
plain-text caption. It performs local Manim construction and layout only.

## Why this is the correct next step

Checkpoint 26 completed a stable linear-combination lesson frame containing:

```text
completed resultant trace
moving term and resultant arrows
synchronized numerical readout
moving mathematical segment labels
```

The first complete chapter also needs moments where the visual behavior is tied
to a concise mathematical statement. The repository already contains broad
scene helpers such as `chapter_title(...)` and `pause_and_predict(...)`, so this
checkpoint should not duplicate title, prompt, or chapter orchestration.

The smallest missing primitive is a reusable equation callout that can later
present a statement such as:

```text
w = a u + b v
```

with an optional explanation. As with the label workflow, this checkpoint
proves the component independently before a later scene decides when and where
it appears.

## Architectural position

```text
scene-owned pedagogical sequencing
              |
              +-- ManimLinearCombinationPresentation
              +-- ManimLinearCombinationLabels
              +-- ManimLinearCombinationTrace
              `-- ManimEquationCallout
```

The callout is independent of the renderer-independent mathematical pipeline.
It does not consume geometry or display snapshots and does not join an existing
moving composite.

## Public interface

```python
callout = ManimEquationCallout(
    r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}",
    caption="Each coefficient scales one vector.",
    content_buff=0.18,
    panel_buff=0.22,
    equation_kwargs={"font_size": 36},
    caption_kwargs={"font_size": 22},
    panel_kwargs={"stroke_width": 1.5},
)
```

The component exposes:

```text
mobject
equation_mobject
caption_mobject
panel_mobject
content_mobjects
equation_source
caption_text
content_buff
panel_buff
equation_kwargs
caption_kwargs
panel_kwargs
```

## Layout and ownership contract

The root object is a `VGroup` whose public child order is:

```text
panel
equation
optional caption
```

When present, the caption is placed below the equation. A
`SurroundingRectangle` encloses the complete content with configurable padding.
The component retains fixed mobject identities and immutable source strings.

Default appearance uses the existing project theme:

```text
equation: TEXT
caption:  MUTED
panel:    PANEL fill with GRID stroke
```

## Validation contract

Before constructing any Manim object, the component validates:

- nonempty equation source;
- optional nonempty caption text;
- finite nonnegative content and panel spacing;
- mapping-based constructor options;
- reserved constructor-owned arguments are not overridden through option maps.

All option mappings are copied. Public option properties return defensive
copies.

## Responsibility boundary

The component does:

- construct one fixed `MathTex` equation;
- optionally construct one fixed explanatory `Text` caption;
- arrange the caption below the equation;
- construct one surrounding panel;
- expose fixed children, source text, spacing, and copied options.

The component does not:

- compute or validate mathematical truth;
- derive equation text from snapshots;
- interpret coefficients, vectors, or geometry;
- animate itself;
- decide screen placement;
- decide when it appears or disappears;
- coordinate a lesson or chapter.

## Files

All files are additive:

```text
CHECKPOINT_27.md
engine/manim_equation_callout.py
tests/test_manim_equation_callout.py
scripts/check_manim_equation_callout.zsh
```

This checkpoint does not modify:

```text
engine/__init__.py
engine/manim_linear_combination_labels.py
engine/manim_linear_combination_presentation.py
scenes/linear_combination_presentation_smoke.py
```

## Focused verification

The focused tests cover:

- root and child ownership;
- equation-only and equation-plus-caption structures;
- source and spacing retention;
- caption placement below the equation;
- panel enclosure of all content;
- copied and observable constructor options;
- defensive option-property copies;
- independence of distinct callout instances;
- equation, caption, spacing, mapping, and reserved-key validation.

The zsh script adds the repository root to `PYTHONPATH`, runs the focused test
file, and then runs the complete repository suite.

## Render decision

Checkpoint 27 adds no scene and changes no scene. Therefore it adds no render
script. A real render is appropriate when a later checkpoint integrates the
proved callout into the linear-combination lesson.

## Next checkpoint

Checkpoint 28 can integrate `ManimEquationCallout` into the existing labeled
linear-combination presentation scene as a static scene-level sibling. The
scene should own its placement and appearance timing, and the callout should
remain outside the one-snapshot-per-frame moving group.
