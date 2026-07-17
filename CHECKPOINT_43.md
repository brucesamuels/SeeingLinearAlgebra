# Engine v0.3 - Checkpoint 43

## Goal

Create the renderer-independent foundation for Chapter 1's introductory lesson:

```text
What Is a Vector?
```

Checkpoint 43 does not build the final Manim lesson. It first defines one
mathematical object whose geometric and coordinate views remain synchronized.

## New mathematical abstraction

```text
VectorRepresentation
VectorRepresentationSnapshot
```

The snapshot contains:

- coordinate array;
- row-coordinate tuple;
- column-coordinate tuple;
- geometric origin;
- geometric endpoint;
- magnitude;
- dimension;
- zero-vector status.

All views are derived from one coordinate vector.

## Central invariant

For vector `v` drawn from origin `p`:

```text
endpoint = p + v
```

Changing the drawing origin changes the vector's location but not its
coordinates as a free vector.

## Why this abstraction is justified

The introductory lesson must connect several views of the same object:

```text
geometric arrow
coordinate row
coordinate column
magnitude
dimension
```

Those are not separate mathematical objects. They are synchronized
representations of one vector.

Keeping this synchronization renderer-independent allows future adapters to
display the same snapshot in:

- Manim;
- an interactive web view;
- static diagrams;
- documentation;
- tests.

## New lesson metadata

```text
VECTOR_REPRESENTATION_LESSON_SEQUENCE
```

uses the existing pedagogical vocabulary:

```text
ORIENT
PREDICT
OBSERVE
STABILIZE
REFLECT
```

Its lesson-specific progression is:

```text
introduce geometric arrow
predict coordinate change
synchronize arrow and coordinates
stabilize equivalent views
reflect on vector identity
```

## Architectural boundary

Checkpoint 43 does not add:

- Manim;
- camera behavior;
- animation timing;
- a display adapter;
- a scene;
- chapter execution;
- coordinate-label layout;
- a new lesson framework.

It establishes only the synchronized mathematical state and lesson intent.

## Files

```text
CHECKPOINT_43.md
engine/vector_representation.py
engine/vector_representation_lesson.py
tests/test_vector_representation.py
tests/test_vector_representation_lesson.py
scripts/check_vector_representation.zsh
```

All files are additive.

## Tests

The focused tests verify:

- synchronization of arrow and coordinate views;
- translation invariance of free-vector coordinates;
- scalar reuse;
- zero-vector detection;
- dimension independence;
- immutable arrays and snapshots;
- invalid-coordinate rejection;
- endpoint consistency;
- reuse of the existing lesson-role vocabulary.

## Expected test count

Checkpoint 42 passed 523 tests.

Checkpoint 43 adds 16 collected test cases, for an expected total near:

```text
539 passed
```

## Render decision

No render is required.

## Next checkpoint

Checkpoint 44 should add a renderer-independent display snapshot and projector
for `VectorRepresentationSnapshot`.

That layer should decide only what display-ready values exist, such as:

- 2D or 3D projected endpoints;
- formatted row and column coordinates;
- magnitude text;
- zero-vector annotation.

It should not yet define Manim layout or animation.
