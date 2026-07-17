# Engine v0.3 - Checkpoint 38

## Goal

Add a machine-readable JSON export and structural validation for the
renderer-independent lesson inventory.

Checkpoint 38 is the second read-only consumer of the lesson metadata layer.

## New capabilities

```text
LessonInventoryValidation
validate_lesson_inventory(...)
lesson_inventory_to_dict(...)
lesson_inventory_to_json(...)
```

The validation report records:

- whether the inventory is valid;
- validation errors;
- lesson count;
- total beat count.

The JSON export records:

- schema version;
- lesson count;
- total beat count;
- validation status;
- validation errors;
- ordered lessons;
- ordered beats with stable one-based indices.

## Generated artifact

The command:

```zsh
python scripts/generate_lesson_inventory_json.py
```

writes:

```text
LESSON_INVENTORY.json
```

The output is deterministic:

- keys are sorted;
- indentation is stable;
- lesson and beat order come from the explicit catalog;
- the file ends with one newline.

## Freshness check

The command:

```zsh
python scripts/generate_lesson_inventory_json.py --check
```

fails if the JSON file is missing or differs from the current canonical export.

## Architectural boundary

Checkpoint 38 does not:

- import Manim;
- import scene modules;
- render lessons;
- execute lessons;
- define chapter order;
- discover modules dynamically;
- add callbacks;
- modify the lesson catalog;
- modify scene metadata;
- change the lesson sequence API.

The data flow remains read-only:

```text
LessonSequence
    -> LessonCatalog
    -> LessonInventory
    -> Validation
    -> JSON
```

## Files

```text
CHECKPOINT_38.md
engine/lesson_inventory_json.py
scripts/generate_lesson_inventory_json.py
scripts/check_lesson_inventory_json.zsh
tests/test_lesson_inventory_json.py
tests/test_generate_lesson_inventory_json.py
```

The verification script generates:

```text
LESSON_INVENTORY.json
```

All source files are additive.

## Tests

The focused tests verify:

- valid-inventory reporting;
- malformed inventory detection;
- stable schema version;
- deterministic and parseable JSON;
- beat ordering and indices;
- argument validation;
- file generation;
- freshness checking;
- stale-file detection.

## Expected test count

Checkpoint 37 passed 480 tests.

Checkpoint 38 adds eight focused test cases, for an expected total near:

```text
488 passed
```

## Render decision

No render is required. Checkpoint 38 consumes renderer-independent metadata only.

## Next checkpoint

Checkpoint 39 should use the Markdown and JSON inventories together in a small
consistency check or documentation verification command.

A chapter framework remains premature. The current goal is to establish that
the lesson metadata is reliable, inspectable, and useful to tooling before it
is used for composition.
