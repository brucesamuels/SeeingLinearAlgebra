# Engine v0.3 - Checkpoint 47

## Goal

Teach the free-vector concept explicitly:

```text
equal vectors may appear at different locations
```

Checkpoint 47 separates this objective from the earlier equivalent-
representations lesson.

## New renderer-independent model

```text
FreeVectorEquality
FreeVectorEqualitySnapshot
```

The model creates translated copies of one vector and verifies that all copies
preserve:

- coordinates;
- dimension;
- magnitude.

The copies may have different origins and endpoints.

## Lesson sequence

```text
ORIENT
show one vector

PREDICT
ask whether moving the arrow changes the vector

OBSERVE
translate the arrow through several locations

STABILIZE
compare same coordinates, direction, and magnitude

REFLECT
state the definition of free-vector equality
```

## Presentation scene

```text
FreeVectorEqualityPresentation
```

The scene animates one arrow through several translated positions, then displays
all copies simultaneously.

## Architectural boundary

The mathematical layer owns equality invariants and translated snapshots.

The scene owns:

- arrow motion;
- reveal order;
- prompts;
- explanatory text;
- timing.

The scene does not recompute vector equality.

## Files

```text
CHECKPOINT_47.md
engine/free_vector_equality.py
engine/free_vector_equality_lesson.py
scenes/free_vector_equality_presentation.py
tests/test_free_vector_equality.py
tests/test_free_vector_equality_lesson.py
tests/test_free_vector_equality_presentation.py
scripts/check_free_vector_equality.zsh
scripts/render_free_vector_equality_presentation.zsh
```

## Verification

```zsh
./scripts/check_free_vector_equality.zsh
./scripts/render_free_vector_equality_presentation.zsh
```

## Next checkpoint

If the render communicates equality clearly, CP48 should register both
introductory vector lessons in the canonical lesson catalog and attach them to
the first Chapter 1 section.
