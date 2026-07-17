# Engine v0.3 - Checkpoint 36

## Goal

Add lightweight, renderer-independent inspection of the lesson sequences proven
in Checkpoints 33-35.

Checkpoint 36 introduces a catalog, not a chapter framework.

## New abstractions

```text
LessonDescriptor
LessonCatalog
```

`LessonDescriptor` associates:

- a stable key;
- a human-readable title;
- an existing `LessonSequence`.

`LessonCatalog` provides:

- immutable declared order;
- unique keys;
- lookup by key;
- titles and keys for documentation or tooling.

## Canonical project catalog

```python
SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
```

initially contains:

```text
full_rank_3d_linear_combination
rank_collapse
```

The catalog reuses the exact sequence objects already declared by the two
presentation lessons.

## Architectural boundary

The catalog does not:

- import Manim;
- import scenes;
- discover modules dynamically;
- execute lessons;
- define animation order;
- define chapter order;
- define prerequisites;
- define transitions;
- define narration;
- register callbacks;
- mutate lesson sequences.

Registration is explicit in one canonical module. This keeps discovery
predictable and prevents import-time scene behavior.

## Why a catalog is justified

Two different lessons now expose stable renderer-independent metadata. A small
inspection layer is useful for:

- documentation generation;
- test reporting;
- future authoring tools;
- verifying available lesson vocabulary;
- later chapter composition, if repeated use justifies it.

A catalog records what exists. It does not decide how lessons are taught or
assembled.

## Files

```text
CHECKPOINT_36.md
engine/lesson_catalog.py
engine/seeing_linear_algebra_lesson_catalog.py
tests/test_lesson_catalog.py
tests/test_seeing_linear_algebra_lesson_catalog.py
scripts/check_lesson_catalog.zsh
```

All files are additive.

## Tests

The focused tests verify:

- frozen normalized descriptors;
- valid `LessonSequence` references;
- nonempty catalogs;
- unique normalized keys;
- immutable order;
- lookup and membership;
- absence of Manim and NumPy imports;
- exact contents of the canonical catalog;
- reuse of the existing full-rank and rank-collapse sequence objects;
- absence of execution and chapter APIs.

## Expected test count

Checkpoint 35 was expected to leave approximately 453 passing tests.

Checkpoint 36 adds 16 focused test cases, for an expected total near:

```text
469 passed
```

The exact count depends on the local repository and parametrization.

## Render decision

No render is required. Checkpoint 36 adds metadata inspection only and modifies
no scene.

## Next checkpoint

Checkpoint 37 should consume the catalog for one useful read-only output, such
as a generated lesson inventory or documentation report.

It should still avoid:

- chapter execution;
- automatic scene discovery;
- orchestration callbacks;
- rendering control.

The catalog API should remain stable while it earns use through tooling.
