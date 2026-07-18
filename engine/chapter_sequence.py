"""Renderer-independent ordering metadata for chapter lesson sequences.

This module records which proven lessons belong to a chapter sequence and in
what order they appear. It intentionally contains no Manim imports, scene
classes, animation behavior, mathematics, or renderer lifecycle code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True, slots=True)
class ChapterLessonReference:
    """Stable renderer-independent reference to one completed lesson."""

    key: str
    title: str

    def __post_init__(self) -> None:
        for attribute_name in ("key", "title"):
            value = getattr(self, attribute_name)
            if not isinstance(value, str):
                raise TypeError(
                    f"chapter lesson {attribute_name} must be a string"
                )

            normalized = value.strip()
            if not normalized:
                raise ValueError(
                    f"chapter lesson {attribute_name} must be nonempty"
                )

            object.__setattr__(self, attribute_name, normalized)


class ChapterSequence:
    """Immutable ordered sequence of renderer-independent lesson references."""

    __slots__ = (
        "_key",
        "_title",
        "_lessons",
        "_lessons_by_key",
    )

    def __init__(
        self,
        *,
        key: str,
        title: str,
        lessons: Iterable[ChapterLessonReference],
    ) -> None:
        self._key = self._normalize_text(key, field_name="chapter key")
        self._title = self._normalize_text(title, field_name="chapter title")

        try:
            normalized_lessons = tuple(lessons)
        except TypeError as exc:
            raise TypeError("chapter lessons must be iterable") from exc

        if not normalized_lessons:
            raise ValueError("chapter sequence must contain at least one lesson")

        lessons_by_key: dict[str, ChapterLessonReference] = {}
        for lesson in normalized_lessons:
            if not isinstance(lesson, ChapterLessonReference):
                raise TypeError(
                    "chapter sequence entries must be "
                    "ChapterLessonReference instances"
                )

            if lesson.key in lessons_by_key:
                raise ValueError(
                    f"chapter lesson keys must be unique: {lesson.key!r}"
                )

            lessons_by_key[lesson.key] = lesson

        self._lessons = normalized_lessons
        self._lessons_by_key = lessons_by_key

    @staticmethod
    def _normalize_text(value: str, *, field_name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")

        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} must be nonempty")

        return normalized

    @property
    def key(self) -> str:
        return self._key

    @property
    def title(self) -> str:
        return self._title

    @property
    def lessons(self) -> tuple[ChapterLessonReference, ...]:
        return self._lessons

    @property
    def lesson_keys(self) -> tuple[str, ...]:
        return tuple(lesson.key for lesson in self._lessons)

    @property
    def lesson_titles(self) -> tuple[str, ...]:
        return tuple(lesson.title for lesson in self._lessons)

    def lesson(self, key: str) -> ChapterLessonReference:
        normalized = self._normalize_text(key, field_name="lesson lookup key")

        try:
            return self._lessons_by_key[normalized]
        except KeyError as exc:
            raise KeyError(f"unknown chapter lesson: {normalized!r}") from exc

    def has_lesson(self, key: str) -> bool:
        if not isinstance(key, str):
            raise TypeError("lesson lookup key must be a string")

        normalized = key.strip()
        return bool(normalized) and normalized in self._lessons_by_key

    def __len__(self) -> int:
        return len(self._lessons)

    def __iter__(self) -> Iterator[ChapterLessonReference]:
        return iter(self._lessons)

    def __getitem__(
        self,
        index: int | slice,
    ) -> ChapterLessonReference | tuple[ChapterLessonReference, ...]:
        return self._lessons[index]

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self.has_lesson(key)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(key={self._key!r}, "
            f"title={self._title!r}, lessons={self._lessons!r})"
        )
