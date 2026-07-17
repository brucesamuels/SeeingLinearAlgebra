# Engine v0.3 - Checkpoint 39

## Goal

Consolidate lesson-documentation verification into one read-only command.

Checkpoint 39 verifies that:

- `LESSON_INVENTORY.md` is current;
- `LESSON_INVENTORY.json` is current;
- both are derived from the same canonical lesson inventory;
- lesson counts and beat counts agree;
- lesson keys and titles agree;
- beat names and roles agree in exact order.

## New abstraction

```text
LessonDocumentationVerification
```

and two verification functions:

```python
verify_lesson_documentation(...)
verify_lesson_documentation_files(...)
```

The verifier compares generated documentation against the canonical
`LessonInventory`. It does not infer truth from one generated format alone.

## Unified command

```zsh
python scripts/verify_lesson_documentation.py
```

reports success only when both files exist, are current, and remain semantically
consistent.

The complete checkpoint script is:

```zsh
./scripts/check_lesson_documentation.zsh
```

It:

1. regenerates both inventories;
2. runs each individual freshness check;
3. runs the cross-format verifier;
4. runs focused tests;
5. runs the full suite.

## Architectural boundary

Checkpoint 39 does not:

- import Manim;
- import scene modules;
- execute lessons;
- render lessons;
- discover lessons dynamically;
- modify the catalog;
- define chapter order;
- define transitions;
- add callbacks;
- add orchestration behavior.

The documentation pipeline remains:

```text
LessonSequence
    -> LessonCatalog
    -> LessonInventory
    -> Markdown + JSON
    -> Verification
```

Every stage is deterministic and read-only with respect to engine behavior.

## Files

```text
CHECKPOINT_39.md
engine/lesson_documentation_verification.py
scripts/verify_lesson_documentation.py
scripts/check_lesson_documentation.zsh
tests/test_lesson_documentation_verification.py
tests/test_verify_lesson_documentation_script.py
```

All source files are additive.

## Tests

The focused tests verify:

- acceptance of current consistent formats;
- stale Markdown detection;
- stale JSON detection;
- malformed JSON detection;
- missing-file reporting;
- valid-file verification;
- argument validation;
- command-line success;
- command-line failure for stale files.

## Expected test count

Checkpoint 38 passed 488 tests.

Checkpoint 39 adds nine focused test cases, for an expected total near:

```text
497 passed
```

## Render decision

No render is required.

## Architectural result

The lesson metadata layer now has:

- two real scene integrations;
- an explicit catalog;
- a human-readable inventory;
- a machine-readable inventory;
- structural validation;
- unified documentation verification.

This is enough evidence to freeze the read-only tooling layer.

## Next checkpoint

Checkpoint 40 should mark an intentional transition away from metadata tooling.

The best next step is to inspect the original Chapter 1 storyboard or lesson
plan and identify the smallest composition concept justified by actual chapter
content.

No chapter runner should be implemented until the storyboard is available and
its repeated structure has been inspected.
