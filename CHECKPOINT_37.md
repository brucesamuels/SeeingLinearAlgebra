# Engine v0.3 - Checkpoint 37

## Goal

Create the first useful read-only consumer of the renderer-independent lesson
catalog.

Checkpoint 37 generates a deterministic Markdown inventory of the lessons and
pedagogical beats currently declared by the engine.

## New abstractions

```text
LessonInventoryEntry
LessonInventory
```

The inventory is derived from `LessonCatalog`. It does not replace or mutate the
catalog.

Each inventory entry contains:

- lesson key;
- lesson title;
- ordered beat names;
- ordered role values.

## Generated artifact

The command:

```zsh
python scripts/generate_lesson_inventory.py
```

writes:

```text
LESSON_INVENTORY.md
```

The generated report contains:

- total lesson count;
- total beat count;
- one section per lesson;
- one ordered table of beats and roles per lesson.

The output is deterministic and therefore suitable for version control.

## Freshness check

The command:

```zsh
python scripts/generate_lesson_inventory.py --check
```

compares the current catalog-derived output with the existing report and fails
when the report is missing or stale.

This provides a small foundation for future documentation automation without
introducing dynamic discovery.

## Architectural boundary

Checkpoint 37 does not:

- import Manim;
- import scene modules;
- execute a lesson;
- render anything;
- define chapter order;
- define transitions;
- register callbacks;
- introspect source code;
- discover lessons dynamically;
- mutate catalog entries.

The data flow remains:

```text
LessonSequence
    -> LessonDescriptor
    -> LessonCatalog
    -> LessonInventory
    -> Markdown report
```

Every arrow is read-only.

## Files

```text
CHECKPOINT_37.md
engine/lesson_inventory.py
scripts/generate_lesson_inventory.py
scripts/check_lesson_inventory.zsh
tests/test_lesson_inventory.py
tests/test_generate_lesson_inventory.py
```

The verification script also creates:

```text
LESSON_INVENTORY.md
```

All source files are additive.

## Tests

The focused tests verify:

- correct descriptor-to-entry conversion;
- catalog-order preservation;
- aggregate lesson and beat counts;
- deterministic Markdown;
- heading validation;
- absence of execution APIs;
- report generation;
- report freshness checking;
- stale-report detection.

## Expected test count

Checkpoint 36 passed 470 tests locally.

Checkpoint 37 adds 10 focused test cases, for an expected total near:

```text
480 passed
```

## Render decision

No render is required. The checkpoint reads renderer-independent metadata and
generates documentation only.

## Next checkpoint

Checkpoint 38 should use the inventory in one additional non-executing way,
such as a machine-readable JSON export or a validation report.

A chapter abstraction is still premature. The immediate goal is to prove that
the metadata layer supports useful tooling while remaining independent of scene
execution.
