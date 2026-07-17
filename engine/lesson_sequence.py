"""Renderer-independent pedagogical sequencing metadata.

This module deliberately describes lesson structure without executing it.
It contains no mathematics, geometry, projection, Manim, animation, timing,
callback, or scene-lifecycle behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator


class LessonBeatRole(str, Enum):
    """Stable pedagogical roles used to describe a lesson progression."""

    ORIENT = "orient"
    PREDICT = "predict"
    OBSERVE = "observe"
    STABILIZE = "stabilize"
    REFLECT = "reflect"


@dataclass(frozen=True, slots=True)
class LessonBeat:
    """One named pedagogical beat in a lesson sequence."""

    name: str
    role: LessonBeatRole

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("lesson beat name must be a string")

        normalized_name = self.name.strip()
        if not normalized_name:
            raise ValueError("lesson beat name must be nonempty")

        if not isinstance(self.role, LessonBeatRole):
            raise TypeError("lesson beat role must be a LessonBeatRole")

        object.__setattr__(self, "name", normalized_name)


class LessonSequence:
    """Immutable ordered metadata describing a pedagogical progression.

    The sequence intentionally does not execute scene methods or animations.
    A renderer-specific scene remains responsible for implementing each beat
    explicitly and readably.
    """

    __slots__ = ("_beats", "_beats_by_name")

    def __init__(self, beats: Iterable[LessonBeat]) -> None:
        try:
            normalized_beats = tuple(beats)
        except TypeError as exc:
            raise TypeError("lesson sequence beats must be iterable") from exc

        if not normalized_beats:
            raise ValueError("lesson sequence must contain at least one beat")

        beats_by_name: dict[str, LessonBeat] = {}
        for beat in normalized_beats:
            if not isinstance(beat, LessonBeat):
                raise TypeError(
                    "lesson sequence entries must be LessonBeat instances"
                )
            if beat.name in beats_by_name:
                raise ValueError(
                    f"lesson beat names must be unique: {beat.name!r}"
                )
            beats_by_name[beat.name] = beat

        self._beats = normalized_beats
        self._beats_by_name = beats_by_name

    @property
    def beats(self) -> tuple[LessonBeat, ...]:
        """Return the immutable ordered beat tuple."""
        return self._beats

    @property
    def names(self) -> tuple[str, ...]:
        """Return beat names in declared order."""
        return tuple(beat.name for beat in self._beats)

    @property
    def roles(self) -> tuple[LessonBeatRole, ...]:
        """Return pedagogical roles in declared order."""
        return tuple(beat.role for beat in self._beats)

    def beat(self, name: str) -> LessonBeat:
        """Return the beat with *name*.

        Raises:
            TypeError: if *name* is not a string.
            KeyError: if no beat has the normalized name.
        """
        if not isinstance(name, str):
            raise TypeError("lesson beat lookup name must be a string")

        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("lesson beat lookup name must be nonempty")

        try:
            return self._beats_by_name[normalized_name]
        except KeyError as exc:
            raise KeyError(f"unknown lesson beat: {normalized_name!r}") from exc

    def has_beat(self, name: str) -> bool:
        """Return whether the sequence contains *name*."""
        if not isinstance(name, str):
            raise TypeError("lesson beat lookup name must be a string")
        normalized_name = name.strip()
        if not normalized_name:
            return False
        return normalized_name in self._beats_by_name

    def beats_with_role(
        self, role: LessonBeatRole
    ) -> tuple[LessonBeat, ...]:
        """Return all beats with *role*, preserving declared order."""
        if not isinstance(role, LessonBeatRole):
            raise TypeError("lesson beat role must be a LessonBeatRole")
        return tuple(beat for beat in self._beats if beat.role is role)

    def __len__(self) -> int:
        return len(self._beats)

    def __iter__(self) -> Iterator[LessonBeat]:
        return iter(self._beats)

    def __getitem__(self, index: int | slice) -> LessonBeat | tuple[LessonBeat, ...]:
        return self._beats[index]

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and self.has_beat(name)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(beats={self._beats!r})"
