"""Read-only inventory generation for renderer-independent lesson metadata."""

from __future__ import annotations

from dataclasses import dataclass

from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.lesson_sequence import LessonBeat


@dataclass(frozen=True, slots=True)
class LessonInventoryEntry:
    """Serializable inspection view of one lesson descriptor."""

    key: str
    title: str
    beat_names: tuple[str, ...]
    beat_roles: tuple[str, ...]

    @classmethod
    def from_descriptor(
        cls, descriptor: LessonDescriptor
    ) -> "LessonInventoryEntry":
        return cls(
            key=descriptor.key,
            title=descriptor.title,
            beat_names=descriptor.sequence.names,
            beat_roles=tuple(
                role.value for role in descriptor.sequence.roles
            ),
        )


@dataclass(frozen=True, slots=True)
class LessonInventory:
    """Immutable inventory derived from a lesson catalog."""

    entries: tuple[LessonInventoryEntry, ...]

    @classmethod
    def from_catalog(cls, catalog: LessonCatalog) -> "LessonInventory":
        if not isinstance(catalog, LessonCatalog):
            raise TypeError("catalog must be a LessonCatalog")
        return cls(
            tuple(
                LessonInventoryEntry.from_descriptor(descriptor)
                for descriptor in catalog
            )
        )

    @property
    def lesson_count(self) -> int:
        return len(self.entries)

    @property
    def total_beat_count(self) -> int:
        return sum(len(entry.beat_names) for entry in self.entries)

    def to_markdown(self, *, heading: str = "Lesson Inventory") -> str:
        if not isinstance(heading, str):
            raise TypeError("heading must be a string")

        normalized_heading = heading.strip()
        if not normalized_heading:
            raise ValueError("heading must be nonempty")

        lines = [
            f"# {normalized_heading}",
            "",
            f"Lessons: {self.lesson_count}",
            f"Total beats: {self.total_beat_count}",
            "",
        ]

        for entry in self.entries:
            lines.extend(
                [
                    f"## {entry.title}",
                    "",
                    f"Key: `{entry.key}`",
                    "",
                    "| # | Beat | Role |",
                    "|---:|---|---|",
                ]
            )

            for index, (name, role) in enumerate(
                zip(entry.beat_names, entry.beat_roles),
                start=1,
            ):
                lines.append(f"| {index} | `{name}` | `{role}` |")

            lines.append("")

        return "\n".join(lines).rstrip() + "\n"
