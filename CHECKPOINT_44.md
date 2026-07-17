# Engine v0.3 - Checkpoint 44

## Goal

Add the renderer-independent display layer for the introductory vector lesson.

Checkpoint 43 established one synchronized mathematical vector representation.
Checkpoint 44 projects that state into display-ready values without introducing
Manim, layout, or animation.

## New abstractions

```text
VectorRepresentationDisplaySnapshot
VectorRepresentationDisplayProjector
```

The display snapshot contains:

- projected origin;
- projected endpoint;
- projected vector;
- formatted row-coordinate text;
- formatted column-coordinate entries;
- formatted magnitude text;
- dimension text;
- optional zero-vector annotation;
- source dimension;
- display dimension.

## Projection behavior

A source vector may have any positive dimension.

The display projector supports:

```text
2D display
3D display
```

For higher-dimensional vectors, geometric display uses the first two or three
coordinates while coordinate text preserves every source coordinate.

For example:

```text
source coordinates: [1, 2, 3, 4]
2D projected vector: [1, 2]
column display: 1, 2, 3, 4
source dimension: 4
display dimension: 2
```

This keeps the mathematical object dimension-independent while acknowledging
that geometric renderers display only two or three spatial dimensions.

## Formatting responsibility

The projector owns display-ready strings such as:

```text
[3.0, 4.0]
magnitude = 5.0
dimension = 2
zero vector
```

It does not own:

- font selection;
- colors;
- screen positions;
- braces or matrix mobjects;
- animation timing;
- camera behavior.

Those remain renderer concerns.

## Central invariant

The projected geometry preserves:

```text
projected endpoint
=
projected origin + projected vector
```

## Architectural boundary

Checkpoint 44 does not add:

- Manim imports;
- a Manim adapter;
- scene code;
- layout;
- animation;
- chapter execution;
- new mathematics.

The data flow is now:

```text
VectorRepresentation
    -> VectorRepresentationSnapshot
    -> VectorRepresentationDisplayProjector
    -> VectorRepresentationDisplaySnapshot
```

## Files

```text
CHECKPOINT_44.md
engine/vector_representation_display.py
tests/test_vector_representation_display.py
scripts/check_vector_representation_display.zsh
```

All files are additive.

## Tests

The focused tests verify:

- synchronized 2D projection;
- translated origins;
- higher-dimensional source projection;
- 3D projection;
- zero-vector annotation;
- configurable formatting;
- configurable magnitude label;
- invalid display dimensions;
- invalid number formats;
- insufficient source dimensions;
- immutable display snapshots;
- projected endpoint consistency.

## Expected test count

Checkpoint 43 passed 538 tests.

Checkpoint 44 adds 15 collected test cases, for an expected total near:

```text
553 passed
```

## Render decision

No render is required.

## Next checkpoint

Checkpoint 45 should introduce a thin Manim adapter for
`VectorRepresentationDisplaySnapshot`.

The adapter should build:

- one arrow;
- one row-coordinate display;
- one column-coordinate display;
- one magnitude label;
- one optional zero-vector annotation.

It should not yet own lesson timing. A smoke scene may then verify that all views
render together before the complete lesson scene is assembled.
