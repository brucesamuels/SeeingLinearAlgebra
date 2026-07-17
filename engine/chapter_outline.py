"""Renderer-independent chapter-outline metadata.

A chapter outline records ordered instructional sections and optional references
to cataloged lessons. It does not execute, render, schedule, or discover scenes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

from engine.lesson_catalog import LessonCatalog


@dataclass(frozen=True, slots=True)
class ChapterSection:
    """One ordered instructional section in a chapter outline."""

    key: str
    title: str
    purpose: str
    lesson_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for attribute_name in ("key", "title", "purpose"):
            value = getattr(self, attribute_name)
            if not isinstance(value, str):
                raise TypeError(f"chapter section {attribute_name} must be a string")
            normalized = value.strip()
            if not normalized:
                raise ValueError(
                    f"chapter section {attribute_name} must be nonempty"
                )
            object.__setattr__(self, attribute_name, normalized)

        try:
            normalized_lesson_keys = tuple(self.lesson_keys)
        except TypeError as exc:
            raise TypeError("chapter section lesson_keys must be iterable") from exc

        cleaned: list[str] = []
        seen: set[str] = set()
        for lesson_key in normalized_lesson_keys:
            if not isinstance(lesson_key, str):
                raise TypeError("chapter section lesson keys must be strings")
            normalized = lesson_key.strip()
            if not normalized:
                raise ValueError("chapter section lesson keys must be nonempty")
            if normalized in seen:
                raise ValueError(
                    f"chapter section lesson keys must be unique: {normalized!r}"
                )
            seen.add(normalized)
            cleaned.append(normalized)

        object.__setattr__(self, "lesson_keys", tuple(cleaned))


class ChapterOutline:
    """Immutable ordered chapter metadata with optional lesson references."""

    __slots__ = ("_key", "_title", "_sections", "_by_key")

    def __init__(
        self,
        *,
        key: str,
        title: str,
        sections: Iterable[ChapterSection],
    ) -> None:
        self._key = self._normalize_text(key, "chapter key")
        self._title = self._normalize_text(title, "chapter title")

        try:
            normalized_sections = tuple(sections)
        except TypeError as exc:
            raise TypeError("chapter sections must be iterable") from exc

        if not normalized_sections:
            raise ValueError("chapter outline must contain at least one section")

        by_key: dict[str, ChapterSection] = {}
        for section in normalized_sections:
            if not isinstance(section, ChapterSection):
                raise TypeError(
                    "chapter outline entries must be ChapterSection instances"
                )
            if section.key in by_key:
                raise ValueError(
                    f"chapter section keys must be unique: {section.key!r}"
                )
            by_key[section.key] = section

        self._sections = normalized_sections
        self._by_key = by_key

    @staticmethod
    def _normalize_text(value: str, label: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{label} must be nonempty")
        return normalized

    @property
    def key(self) -> str:
        return self._key

    @property
    def title(self) -> str:
        return self._title

    @property
    def sections(self) -> tuple[ChapterSection, ...]:
        return self._sections

    @property
    def section_keys(self) -> tuple[str, ...]:
        return tuple(section.key for section in self._sections)

    @property
    def referenced_lesson_keys(self) -> tuple[str, ...]:
        return tuple(
            lesson_key
            for section in self._sections
            for lesson_key in section.lesson_keys
        )

    def section(self, key: str) -> ChapterSection:
        normalized = self._normalize_text(key, "chapter section lookup key")
        try:
            return self._by_key[normalized]
        except KeyError as exc:
            raise KeyError(f"unknown chapter section: {normalized!r}") from exc

    def validate_lesson_references(
        self,
        catalog: LessonCatalog,
    ) -> tuple[str, ...]:
        """Return unknown lesson keys without mutating the outline."""
        if not isinstance(catalog, LessonCatalog):
            raise TypeError("catalog must be a LessonCatalog")
        return tuple(
            key
            for key in self.referenced_lesson_keys
            if not catalog.has_lesson(key)
        )

    def __len__(self) -> int:
        return len(self._sections)

    def __iter__(self) -> Iterator[ChapterSection]:
        return iter(self._sections)

    def __getitem__(
        self, index: int | slice
    ) -> ChapterSection | tuple[ChapterSection, ...]:
        return self._sections[index]

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"key={self.key!r}, title={self.title!r}, "
            f"sections={self.sections!r})"
        )
