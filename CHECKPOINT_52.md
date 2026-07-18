# Engine v0.3 - Checkpoint 52

## Goal

Begin assembling Chapter 1 by defining an explicit, renderer-independent order
for the first three completed lessons:

```text
Why Vectors?
What Is a Vector?
Free Vectors and Equality
```

Checkpoint 52 records chapter membership and order only. It does not yet
combine Manim scenes or alter any approved lesson presentation.

## New abstractions

```text
ChapterLessonReference
ChapterSequence
```

`ChapterLessonReference` identifies one completed lesson through a stable key
and title.

`ChapterSequence` owns:

- one stable chapter key;
- one chapter title;
- an immutable ordered tuple of lesson references;
- exact lesson-key and lesson-title order;
- lookup and membership by lesson key;
- validation of nonempty metadata and unique lesson keys.

## Chapter 1 opening sequence

The canonical opening sequence is:

```python
CHAPTER_ONE_OPENING_SEQUENCE
```

with the order:

```text
why_vectors
vector_representation
free_vector_equality
```

and the display titles:

```text
Why Vectors?
What Is a Vector?
Free Vectors and Equality
```

## Architectural boundary

The chapter sequence is renderer-independent. It contains no:

- Manim imports;
- scene classes;
- animation timing;
- mathematical snapshots;
- geometry or projection;
- presentation execution;
- dynamic scene discovery.

The existing lesson catalog remains an inventory of proven lesson sequences.
The new chapter sequence serves a different responsibility: explicit
curricular order.

The three completed presentation scenes remain unchanged and independently
renderable.

## Why there is no combined render yet

A combined Manim presentation would require a renderer-side composition
contract for reusing complete lesson presentations inside one scene. That
contract has not yet been proved.

Checkpoint 52 therefore establishes the renderer-independent source of truth
first. A later checkpoint can add a thin Manim orchestration layer that consumes
this sequence without copying lesson content.

## Files

All files are additive:

```text
CHECKPOINT_52.md
engine/chapter_sequence.py
engine/chapter_one_opening_sequence.py
tests/test_chapter_sequence.py
tests/test_chapter_one_opening_sequence.py
scripts/check_chapter_one_opening_sequence.zsh
```

No existing engine, scene, test, or script file is replaced.

## Verification

```zsh
./scripts/check_chapter_one_opening_sequence.zsh
```

The focused tests cover:

- text normalization and validation;
- immutable declared lesson order;
- indexing, iteration, slicing, lookup, and membership;
- rejection of empty sequences and duplicate lesson keys;
- absence of renderer dependencies;
- the exact approved Chapter 1 opening order.

## Render decision

Checkpoint 52 adds no Manim scene and changes no existing scene. Therefore it
adds no render script.

The established lesson render scripts remain available for individual visual
regression checks.

## Next checkpoint

Checkpoint 53 should add the thinnest renderer-side chapter-opening
orchestration that consumes `CHAPTER_ONE_OPENING_SEQUENCE` and reuses the three
existing lesson presentations without moving chapter order into Manim code.

It should preserve each standalone scene and avoid a general textbook runtime
until the first combined render proves what orchestration behavior is actually
needed.
