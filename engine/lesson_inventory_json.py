"""Machine-readable export and validation for lesson inventories."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from engine.lesson_inventory import LessonInventory


@dataclass(frozen=True, slots=True)
class LessonInventoryValidation:
    """Validation result for one lesson inventory."""

    is_valid: bool
    errors: tuple[str, ...]
    lesson_count: int
    total_beat_count: int


def validate_lesson_inventory(
    inventory: LessonInventory,
) -> LessonInventoryValidation:
    """Validate structural invariants of a derived lesson inventory."""
    if not isinstance(inventory, LessonInventory):
        raise TypeError("inventory must be a LessonInventory")

    errors: list[str] = []
    seen_keys: set[str] = set()

    for entry_index, entry in enumerate(inventory.entries, start=1):
        if entry.key in seen_keys:
            errors.append(f"duplicate lesson key: {entry.key!r}")
        seen_keys.add(entry.key)

        if len(entry.beat_names) != len(entry.beat_roles):
            errors.append(
                f"lesson {entry.key!r} has mismatched beat names and roles"
            )

        if not entry.beat_names:
            errors.append(f"lesson {entry.key!r} has no beats")

        seen_names: set[str] = set()
        for beat_index, name in enumerate(entry.beat_names, start=1):
            if name in seen_names:
                errors.append(
                    f"lesson {entry.key!r} has duplicate beat name: {name!r}"
                )
            seen_names.add(name)

            if not name.strip():
                errors.append(
                    f"lesson {entry.key!r} has empty beat name at "
                    f"position {beat_index}"
                )

        for role_index, role in enumerate(entry.beat_roles, start=1):
            if not role.strip():
                errors.append(
                    f"lesson {entry.key!r} has empty beat role at "
                    f"position {role_index}"
                )

    return LessonInventoryValidation(
        is_valid=not errors,
        errors=tuple(errors),
        lesson_count=inventory.lesson_count,
        total_beat_count=inventory.total_beat_count,
    )


def lesson_inventory_to_dict(
    inventory: LessonInventory,
) -> dict[str, Any]:
    """Return a stable JSON-serializable dictionary for an inventory."""
    if not isinstance(inventory, LessonInventory):
        raise TypeError("inventory must be a LessonInventory")

    validation = validate_lesson_inventory(inventory)

    return {
        "schema_version": 1,
        "lesson_count": inventory.lesson_count,
        "total_beat_count": inventory.total_beat_count,
        "is_valid": validation.is_valid,
        "errors": list(validation.errors),
        "lessons": [
            {
                "key": entry.key,
                "title": entry.title,
                "beats": [
                    {
                        "index": index,
                        "name": name,
                        "role": role,
                    }
                    for index, (name, role) in enumerate(
                        zip(entry.beat_names, entry.beat_roles),
                        start=1,
                    )
                ],
            }
            for entry in inventory.entries
        ],
    }


def lesson_inventory_to_json(
    inventory: LessonInventory,
    *,
    indent: int = 2,
) -> str:
    """Serialize an inventory as deterministic UTF-8 JSON text."""
    if not isinstance(indent, int):
        raise TypeError("indent must be an integer")
    if indent < 0:
        raise ValueError("indent must be nonnegative")

    payload = lesson_inventory_to_dict(inventory)
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=indent,
        sort_keys=True,
    ) + "\n"
