"""Renderer-independent translation of a vector into standard position."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from engine.vector_representation import (
    VectorRepresentation,
    VectorRepresentationSnapshot,
)


FloatArray = NDArray[np.float64]


def _readonly_point(values: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if array.size == 0:
        raise ValueError(f"{name} must contain at least one coordinate")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain finite values")
    result = np.array(array, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _progress_value(progress: float) -> float:
    if not np.isscalar(progress):
        raise TypeError("progress must be a real scalar")
    value = float(progress)
    if not np.isfinite(value):
        raise ValueError("progress must be finite")
    if value < 0.0 or value > 1.0:
        raise ValueError("progress must lie in the closed interval [0, 1]")
    return value


@dataclass(frozen=True, slots=True)
class VectorToOriginTranslationSnapshot:
    """One synchronized state while a vector is translated to the origin."""

    original: VectorRepresentationSnapshot
    current: VectorRepresentationSnapshot
    translation: FloatArray
    progress: float

    def __post_init__(self) -> None:
        if not isinstance(self.original, VectorRepresentationSnapshot):
            raise TypeError("original must be a VectorRepresentationSnapshot")
        if not isinstance(self.current, VectorRepresentationSnapshot):
            raise TypeError("current must be a VectorRepresentationSnapshot")

        progress = _progress_value(self.progress)
        translation = _readonly_point(self.translation, name="translation")

        if self.current.dimension != self.original.dimension:
            raise ValueError("current and original dimensions must match")
        if translation.size != self.original.dimension:
            raise ValueError("translation dimension must match vector dimension")
        if not np.allclose(self.current.coordinates, self.original.coordinates):
            raise ValueError("translation must preserve vector coordinates")

        expected_translation = -progress * self.original.origin
        if not np.allclose(translation, expected_translation):
            raise ValueError("translation must equal -progress times the original tail")
        if not np.allclose(
            self.current.origin,
            self.original.origin + translation,
        ):
            raise ValueError("current initial point does not match translation")
        if not np.allclose(
            self.current.endpoint,
            self.original.endpoint + translation,
        ):
            raise ValueError("current terminal point does not match translation")

        object.__setattr__(self, "translation", translation)
        object.__setattr__(self, "progress", progress)

    @property
    def current_initial_point(self) -> FloatArray:
        return self.current.origin

    @property
    def current_terminal_point(self) -> FloatArray:
        return self.current.endpoint

    @property
    def vector_coordinates(self) -> FloatArray:
        return self.current.coordinates

    @property
    def is_at_origin(self) -> bool:
        return bool(np.allclose(self.current.origin, 0.0))

    @property
    def subtraction_is_invariant(self) -> bool:
        return bool(
            np.allclose(
                self.current.endpoint - self.current.origin,
                self.original.coordinates,
            )
        )


class VectorToOriginTranslation:
    """Translate both endpoints until the vector's tail reaches the origin."""

    __slots__ = (
        "_initial_point",
        "_terminal_point",
        "_required_translation",
        "_vector",
    )

    def __init__(
        self,
        initial_point: ArrayLike,
        terminal_point: ArrayLike,
    ) -> None:
        initial = _readonly_point(initial_point, name="initial_point")
        terminal = _readonly_point(terminal_point, name="terminal_point")
        if terminal.shape != initial.shape:
            raise ValueError("initial and terminal point shapes must match")

        required_translation = np.array(-initial, dtype=float, copy=True)
        required_translation.setflags(write=False)

        self._initial_point = initial
        self._terminal_point = terminal
        self._required_translation = required_translation
        self._vector = VectorRepresentation(
            terminal - initial,
            origin=initial,
        )

    @property
    def initial_point(self) -> FloatArray:
        return self._initial_point

    @property
    def terminal_point(self) -> FloatArray:
        return self._terminal_point

    @property
    def vector_coordinates(self) -> FloatArray:
        return self._vector.coordinates

    @property
    def required_translation(self) -> FloatArray:
        return self._required_translation

    @property
    def dimension(self) -> int:
        return self._vector.dimension

    def snapshot(self, progress: float) -> VectorToOriginTranslationSnapshot:
        progress_value = _progress_value(progress)
        translation = np.array(
            progress_value * self._required_translation,
            dtype=float,
            copy=True,
        )
        translation.setflags(write=False)

        original = self._vector.snapshot()
        current = self._vector.translated_to(
            self._initial_point + translation
        ).snapshot()

        return VectorToOriginTranslationSnapshot(
            original=original,
            current=current,
            translation=translation,
            progress=progress_value,
        )
