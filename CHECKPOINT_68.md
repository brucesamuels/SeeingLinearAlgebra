# Engine v0.3 — Checkpoint 68

## Goal

Begin Chapter 2, **Vector Spaces and Subspaces**, with a standalone visual
lesson that asks:

> What should we call the collection of all vectors we can create?

The checkpoint introduces the span of one vector geometrically before revealing
its formal definition.

## Mathematical narrative

The scene begins with a compact visual echo of the accepted Chapter 1 Living
Vector finale. It does not import, modify, or replay that approved scene.

The lesson then simplifies from many linear combinations to one generator
`v`. A coefficient `t` moves continuously through positive, zero, and negative
values. The endpoint of `t v` leaves a trace. Only after that motion has exposed
the complete line does the scene reveal

```text
span{v} = {t v : t in R}.
```

The final reflection asks why the line must pass through the origin.

## Architecture

```text
OneVectorSpan
    renderer-independent scalar-multiple mathematics
            |
            v
OneVectorSpanSnapshot
            |
            v
ManimOneVectorSpan
    thin identity-preserving arrow and endpoint adapter
            |
            v
OneVectorSpanPresentation
    inquiry, pacing, trace, definition, and reflection
```

The mathematical layer has no Manim dependency. The adapter does not choose
coefficients, perform scalar multiplication, or introduce terminology. The
scene owns choreography and pedagogy.

## Files

All files are additive:

```text
CHECKPOINT_68.md
engine/one_vector_span.py
engine/manim_one_vector_span.py
scenes/one_vector_span_presentation.py
tests/test_one_vector_span.py
tests/test_one_vector_span_presentation.py
scripts/check_one_vector_span.zsh
scripts/render_one_vector_span.zsh
```

No Chapter 1 file is changed.

## Render expectation

The video should show:

1. a short Chapter 2 identity;
2. a visual echo of many generated vectors;
3. the opening inquiry;
4. one fixed blue generator `v`;
5. a yellow `t v` moving continuously in both directions;
6. a persistent endpoint trace revealing a line;
7. the word and definition of span only after the motion;
8. a final reflection pause.

## Visual review priorities

- Does the opening feel like a natural continuation of Living Vector?
- Is the coefficient motion slow enough to make negative multiples intuitive?
- Does the trace read unmistakably as a line through the origin?
- Is the definition delayed long enough?
- Are the lower-screen definition and final reflection comfortably spaced?

## Next checkpoint

After visual approval, Checkpoint 69 should add the two-generator construction:
one coefficient traces a line and the second coefficient slides that line to
sweep out a plane.
