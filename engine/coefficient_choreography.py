"""Renderer-independent choreography through coefficient space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator

import numpy as np
from numpy.typing import ArrayLike, NDArray

from engine.linear_combination import LinearCombination, LinearCombinationSnapshot


FloatArray = NDArray[np.float64]


def _readonly_vector(values: ArrayLike, *, name: str) -> FloatArray:
    array = np.array(values, dtype=float, copy=True)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    array.setflags(write=False)
    return array


@dataclass(frozen=True, slots=True)
class ChoreographedCombination:
    """One coefficient choice and its delegated linear-combination snapshot."""

    coefficients: FloatArray
    snapshot: LinearCombinationSnapshot

    def __post_init__(self) -> None:
        coefficients = _readonly_vector(
            self.coefficients,
            name="coefficients",
        )
        if coefficients.shape != self.snapshot.coefficients.shape:
            raise ValueError("coefficient and snapshot shapes must match")
        if not np.allclose(coefficients, self.snapshot.coefficients):
            raise ValueError("coefficients must match the snapshot")
        object.__setattr__(self, "coefficients", coefficients)


class CoefficientChoreography:
    """Create deterministic samples for a fixed linear combination."""

    def __init__(
        self,
        linear_combination: LinearCombination,
        coefficient_pairs: Iterable[ArrayLike],
    ) -> None:
        if not isinstance(linear_combination, LinearCombination):
            raise TypeError("linear_combination must be a LinearCombination")
        samples = tuple(
            ChoreographedCombination(
                coefficients=coefficients,
                snapshot=linear_combination.snapshot(coefficients),
            )
            for coefficients in coefficient_pairs
        )
        if not samples:
            raise ValueError("at least one coefficient choice is required")
        self._linear_combination = linear_combination
        self._samples = samples

    @property
    def linear_combination(self) -> LinearCombination:
        return self._linear_combination

    @property
    def samples(self) -> tuple[ChoreographedCombination, ...]:
        return self._samples

    def __len__(self) -> int:
        return len(self._samples)

    def __iter__(self) -> Iterator[ChoreographedCombination]:
        return iter(self._samples)


def serpentine_coefficient_grid(
    *,
    a_min: float,
    a_max: float,
    b_min: float,
    b_max: float,
    a_count: int,
    b_count: int,
) -> tuple[FloatArray, ...]:
    """Return a deterministic fine-grid traversal of coefficient space."""

    if a_count < 2 or b_count < 2:
        raise ValueError("grid counts must each be at least two")
    limits = np.array([a_min, a_max, b_min, b_max], dtype=float)
    if not np.all(np.isfinite(limits)):
        raise ValueError("grid limits must be finite")
    if not a_min < a_max or not b_min < b_max:
        raise ValueError("each minimum must be less than its maximum")

    a_values = np.linspace(a_min, a_max, a_count)
    b_values = np.linspace(b_min, b_max, b_count)
    pairs: list[FloatArray] = []
    for row_index, b_value in enumerate(b_values):
        row = a_values if row_index % 2 == 0 else a_values[::-1]
        for a_value in row:
            pair = np.array([a_value, b_value], dtype=float)
            pair.setflags(write=False)
            pairs.append(pair)
    return tuple(pairs)


def selected_story_coefficients() -> tuple[FloatArray, ...]:
    """Return readable examples shown before the dense sweep."""

    choices = (
        (2.0, 1.0),
        (-1.0, 2.0),
        (0.5, -1.5),
        (-2.0, -0.5),
        (1.25, -0.75),
        (1.5, 1.25),
    )
    return tuple(_readonly_vector(choice, name="choice") for choice in choices)



def golden_ratio_coefficient_samples(
    *,
    count: int,
    a_min: float,
    a_max: float,
    b_min: float,
    b_max: float,
) -> tuple[FloatArray, ...]:
    """Return deterministic irregular samples over a coefficient rectangle."""

    if count < 1:
        raise ValueError("count must be positive")
    limits = np.array([a_min, a_max, b_min, b_max], dtype=float)
    if not np.all(np.isfinite(limits)):
        raise ValueError("sample limits must be finite")
    if not a_min < a_max or not b_min < b_max:
        raise ValueError("each minimum must be less than its maximum")

    alpha = (5.0 ** 0.5 - 1.0) / 2.0
    beta = (3.0 ** 0.5 - 1.0) / 2.0
    pairs: list[FloatArray] = []
    for index in range(1, count + 1):
        pair = np.array(
            [
                a_min + ((index * alpha) % 1.0) * (a_max - a_min),
                b_min + ((index * beta) % 1.0) * (b_max - b_min),
            ],
            dtype=float,
        )
        pair.setflags(write=False)
        pairs.append(pair)
    return tuple(pairs)
