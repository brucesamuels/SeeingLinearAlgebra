# Engine v0.3 — Checkpoint 69

## Goal

Continue Chapter 2 by answering:

> What changes when we add a second direction?

The lesson reveals the span of two independent vectors geometrically before
showing its formal definition.

## Mathematical narrative

The scene fixes the coefficient `a` and varies `b` continuously. The endpoint
of

```text
a u + b v
```

moves along one line parallel to `v`. The coefficient `a` then changes, moving
the entire line in the `u` direction. Retained samples of the moving line make
the swept plane visible while the active line continues to move.

Only after the plane has emerged does the scene reveal

```text
span{u, v} = {a u + b v : a, b in R}.
```

## Architecture

```text
TwoVectorSpan
    renderer-independent combinations and fixed-coefficient line families
            |
            v
TwoVectorSpanSnapshot / FixedCoefficientLineSnapshot
            |
            v
ManimTwoVectorCombination / ManimFixedCoefficientLine
    thin identity-preserving adapters
            |
            v
TwoVectorSpanPresentation
    inquiry, coefficient motion, retained sweep, definition, reflection
```

## Files

All files are additive:

```text
CHECKPOINT_69.md
engine/two_vector_span.py
engine/manim_two_vector_span.py
scenes/two_vector_span_presentation.py
tests/test_two_vector_span.py
tests/test_two_vector_span_presentation.py
scripts/check_two_vector_span.zsh
scripts/render_two_vector_span.zsh
```

No approved Chapter 1 or CP68 file is modified.

## Render expectation

The video should show:

1. two independent generator vectors `u` and `v`;
2. the prediction question about gaps, a grid, or the full plane;
3. `b` varying continuously while `a` is fixed;
4. one complete line parallel to `v`;
5. that line sliding continuously in the `u` direction;
6. retained parallel lines revealing the plane;
7. the formal span definition only after the sweep;
8. a reflection about why every point has a coefficient recipe.

## Visual review priorities

- Is it clear that `b` controls motion along one line?
- Is it clear that `a` moves the entire line?
- Does the retained family read as a plane rather than a static grid exercise?
- Is the animation continuous enough to preserve the Chapter 1 visual style?
- Are the readout, labels, and lower-screen text comfortably separated?

## Next checkpoint

After visual approval, Checkpoint 70 should rotate the second generator toward
the first and show the plane collapsing continuously to a line, introducing
linear dependence as the loss of a direction.
