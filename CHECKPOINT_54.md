# Engine v0.3 — Checkpoint 54

## Goal

Add a focused bridge lesson, **Placing a Vector at the Origin**, before the
Chapter 1 vector-operations sequence.

The lesson begins with a general vector on an otherwise blank field. It then
reveals a coordinate system, identifies the initial and terminal points, and
translates both endpoints by the same amount until the tail reaches the origin.
The geometry, endpoint labels, and subtraction panel remain synchronized from
one renderer-independent snapshot per animation frame.

## Mathematical example

The scene uses

```text
initial point  P = (2, 1)
terminal point Q = (5, 3)
```

so

```text
v = Q - P = (5, 3) - (2, 1) = (3, 2).
```

At progress `t`, both endpoints receive the translation

```text
Delta_t = -tP.
```

Therefore

```text
P_t = P + Delta_t
Q_t = Q + Delta_t
Q_t - P_t = Q - P = v.
```

At `t = 1`, the display shows

```text
P_1 = (0, 0)
Q_1 = (3, 2).
```

The vector is unchanged and is now in standard position.

## Architecture

Renderer-independent mathematics:

```text
VectorToOriginTranslation
  -> VectorToOriginTranslationSnapshot
```

Thin Manim display adapter:

```text
ManimVectorToOriginDisplay
```

Presentation sequencing:

```text
PlacingVectorAtOriginPresentation
```

The renderer-independent path is dimension independent. The Manim adapter is
intentionally two-dimensional because this lesson uses a `NumberPlane` and
ordered-pair labels.

## Scene sequence

1. Write the shared lesson title.
2. Draw the vector before any coordinate system is visible.
3. Reveal the coordinate plane.
4. Reveal the initial and terminal points and their coordinates.
5. Ask how to move the tail to the origin without changing the vector.
6. Show the live translation and subtraction panel.
7. Translate the vector while all coordinates and equations update together.
8. Pin the exact final snapshot at the origin.
9. Conclude that the unchanged vector is now in standard position.

## Files

All files are additive:

```text
CHECKPOINT_54.md
engine/vector_to_origin_translation.py
engine/vector_to_origin_lesson.py
engine/manim_vector_to_origin_display.py
scenes/placing_vector_at_origin_presentation.py
tests/test_vector_to_origin_translation.py
tests/test_manim_vector_to_origin_display.py
tests/test_placing_vector_at_origin_presentation.py
scripts/check_placing_vector_at_origin.zsh
scripts/render_placing_vector_at_origin_presentation.zsh
```

No existing lesson or chapter file is modified.

## Verification

The focused tests cover:

- endpoint subtraction and the required translation;
- exact states at progress `0`, `0.5`, and `1`;
- invariant vector coordinates throughout the translation;
- dimension-independent renderer-free mathematics;
- synchronized Manim geometry, endpoint labels, and formula sources;
- identity preservation of the adapter's top-level mobjects;
- vector-first, coordinate-plane-second scene ordering;
- shared theme, layout, text roles, and timing;
- exact final pinning at the origin.

## Render expectation

The visual should show the vector alone first. When the plane appears, its tail
should be at `(2, 1)` and its terminal point at `(5, 3)`. During the three-second
translation, both coordinate labels and the subtraction panel should update in
lockstep with the arrow. The final frame should show the tail at `(0, 0)`, the
terminal point at `(3, 2)`, and the unchanged vector coordinates `(3, 2)`.

## Next checkpoint

After visual approval, the next small checkpoint should insert this proven
lesson into the Chapter 1 opening sequence and combined presentation before any
vector-operation lesson is added.
