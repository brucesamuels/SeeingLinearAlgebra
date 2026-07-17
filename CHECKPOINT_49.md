# Engine v0.3 - Checkpoint 49

## Goal

Introduce the first reusable visual identity system for Seeing Linear Algebra.

Checkpoint 49 adds renderer-side semantic styling only. It adds no mathematics
and no lesson-sequencing behavior.

## New abstractions

```text
LessonColors
LessonTypography
LessonTiming
LessonTheme
SEEING_LINEAR_ALGEBRA_THEME
```

The theme defines semantic roles rather than scene-specific choices.

### Color roles

```text
geometry
application
definition
reflection
prediction
mathematics
example
warning
narration
```

### Typography roles

```text
chapter title
lesson title
guiding question
perspective title
body
takeaway
footer
```

### Timing roles

```text
quick
normal
read
reflection
transition
```

## Instructional widgets

```text
ThemedText
KeyIdeaBanner
```

These are small renderer-side factories and mobject groups that apply semantic
theme roles consistently.

## CP48 integration

The `WhyVectorsPresentation` now uses:

- shared themed typography;
- semantic colors;
- named timing presets;
- the existing shared lesson layout;
- the existing pictogram library.

The lesson content and pedagogical sequence remain unchanged.

## Architectural boundary

Checkpoint 49 does not add:

- chapter execution;
- mathematics;
- scene discovery;
- renderer-independent color semantics;
- a heavyweight widget framework;
- global configuration mutation.

The theme is explicit and injectable.

## Files

```text
CHECKPOINT_49.md
engine/manim_lesson_theme.py
engine/manim_instructional_widgets.py
tests/test_manim_lesson_theme.py
tests/test_manim_instructional_widgets.py
tests/test_why_vectors_theme_integration.py
```

It also updates:

```text
scenes/why_vectors_presentation.py
```

## Verification

```zsh
./scripts/check_why_vectors.zsh

python -m pytest -q \
  tests/test_manim_lesson_theme.py \
  tests/test_manim_instructional_widgets.py \
  tests/test_why_vectors_theme_integration.py

./scripts/render_why_vectors.zsh
```

## Next checkpoint

Checkpoint 50 should migrate one previously completed lesson—preferably
`VectorRepresentationPresentation`—to the same theme and layout.

That will test whether the visual identity system generalizes beyond the
prologue before more widgets are added.
