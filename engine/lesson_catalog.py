"""Renderer-independent catalog of declared lesson sequences.

The catalog supports inspection and documentation. It does not discover scenes
dynamically, import Manim, execute lessons, or define chapter order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

from engine.lesson_sequence import LessonSequence


@dataclass(frozen=True, slots=True)
class LessonDescriptor:
    """One stable catalog entry for a declared lesson sequence."""

    key: str
    title: str
    sequence: LessonSequence

    def __post_init__(self) -> None:
        for attribute_name in ("key", "title"):
            value = getattr(self, attribute_name)
            if not isinstance(value, str):
                raise TypeError(f"lesson {attribute_name} must be a string")
            normalized = value.strip()
            if not normalized:
                raise ValueError(f"lesson {attribute_name} must be nonempty")
            object.__setattr__(self, attribute_name, normalized)

        if not isinstance(self.sequence, LessonSequence):
            raise TypeError("lesson sequence must be a LessonSequence")


class LessonCatalog:
    """Immutable collection of explicitly registered lesson descriptors."""

    __slots__ = ("_lessons", "_by_key")

    def __init__(self, lessons: Iterable[LessonDescriptor]) -> None:
        try:
            normalized = tuple(lessons)
        except TypeError as exc:
            raise TypeError("lesson catalog entries must be iterable") from exc

        if not normalized:
            raise ValueError("lesson catalog must contain at least one lesson")

        by_key: dict[str, LessonDescriptor] = {}
        for lesson in normalized:
            if not isinstance(lesson, LessonDescriptor):
                raise TypeError(
                    "lesson catalog entries must be LessonDescriptor instances"
                )
            if lesson.key in by_key:
                raise ValueError(
                    f"lesson catalog keys must be unique: {lesson.key!r}"
                )
            by_key[lesson.key] = lesson

        self._lessons = normalized
        self._by_key = by_key

    @property
    def lessons(self) -> tuple[LessonDescriptor, ...]:
        return self._lessons

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(lesson.key for lesson in self._lessons)

    @property
    def titles(self) -> tuple[str, ...]:
        return tuple(lesson.title for lesson in self._lessons)

    def lesson(self, key: str) -> LessonDescriptor:
        if not isinstance(key, str):
            raise TypeError("lesson lookup key must be a string")

        normalized = key.strip()
        if not normalized:
            raise ValueError("lesson lookup key must be nonempty")

        try:
            return self._by_key[normalized]
        except KeyError as exc:
            raise KeyError(f"unknown lesson: {normalized!r}") from exc

    def has_lesson(self, key: str) -> bool:
        if not isinstance(key, str):
            raise TypeError("lesson lookup key must be a string")
        normalized = key.strip()
        return bool(normalized) and normalized in self._by_key

    def __len__(self) -> int:
        return len(self._lessons)

    def __iter__(self) -> Iterator[LessonDescriptor]:
        return iter(self._lessons)

    def __getitem__(
        self, index: int | slice
    ) -> LessonDescriptor | tuple[LessonDescriptor, ...]:
        return self._lessons[index]

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self.has_lesson(key)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(lessons={self._lessons!r})"
