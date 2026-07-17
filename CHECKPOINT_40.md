# Engine v0.3 - Checkpoint 40

## Goal

Use actual Chapter 1 instructional content to identify the smallest justified
composition abstraction.

The available lesson progression is:

```text
What Is a Vector?
Scalar Multiplication
Vector Addition
Magnitude
Unit Vectors and the Standard Basis
Linear Combinations and Span
```

Checkpoint 40 records that progression as a read-only chapter outline.

## New abstractions

```text
ChapterSection
ChapterOutline
```

A `ChapterSection` contains:

- a stable key;
- a display title;
- a concise pedagogical purpose;
- zero or more references to existing lesson-catalog keys.

A `ChapterOutline` contains:

- one chapter key;
- one chapter title;
- an immutable ordered section tuple;
- lookup by section key;
- optional validation of lesson references.

## Why this is the smallest justified composition concept

The source material provides evidence for ordered conceptual sections.

It does not yet provide evidence for:

- automatic chapter execution;
- scene transitions;
- narration timing;
- camera coordination across scenes;
- prerequisite graphs;
- branching;
- a chapter superclass;
- a declarative rendering language.

Therefore the first composition abstraction records instructional order and
coverage only.

## Initial Chapter 1 outline

```text
Vectors, Span, and Coordinates

1. What Is a Vector?
2. Scalar Multiplication
3. Vector Addition
4. Magnitude
5. Unit Vectors and the Standard Basis
6. Linear Combinations and Span
```

The two existing cataloged lessons are attached only to the final section:

```text
full_rank_3d_linear_combination
rank_collapse
```

The first five sections intentionally remain without lesson references. This
makes missing engine-driven content visible rather than inventing placeholder
lessons or pretending the chapter is complete.

## Architectural boundary

The outline does not:

- import Manim;
- import scenes;
- execute lessons;
- render a chapter;
- define transitions;
- define timing;
- discover lessons dynamically;
- mutate the lesson catalog;
- require every section to have a lesson;
- claim that catalog order is chapter order.

## Files

```text
CHECKPOINT_40.md
engine/chapter_outline.py
engine/chapter_1_outline.py
tests/test_chapter_outline.py
tests/test_chapter_1_outline.py
scripts/check_chapter_1_outline.zsh
```

All files are additive.

## Tests

The focused tests verify:

- frozen normalized section metadata;
- immutable section ordering;
- unique section keys;
- unique lesson references within a section;
- section lookup;
- catalog-reference validation;
- absence of execution APIs;
- exact Chapter 1 conceptual progression;
- attachment of the two proven lessons to the span section;
- explicit visibility of the five unimplemented content gaps.

## Expected test count

Checkpoint 39 was expected to pass 497 tests.

Checkpoint 40 adds 11 focused test cases, for an expected total near:

```text
508 passed
```

## Render decision

No render is required.

## Architectural result

Checkpoint 40 marks the transition from generic metadata tooling to
content-driven chapter planning.

The engine can now answer two separate questions:

```text
What lessons exist?
What conceptual sections does Chapter 1 require?
```

It does not yet claim that every required section has an engine-driven lesson.

## Next checkpoint

Checkpoint 41 should address the earliest uncovered Chapter 1 section with the
smallest reusable mathematical primitive.

The best candidate is scalar multiplication because:

- it precedes vector addition and linear combinations conceptually;
- the existing linear-combination engine already demonstrates scaled vectors;
- a one-vector coefficient path can likely reuse existing dimension-independent
  mathematics;
- it can be proved independently before any new presentation scene is built.

Checkpoint 41 should inspect existing scalar/vector capabilities before adding
new code.
