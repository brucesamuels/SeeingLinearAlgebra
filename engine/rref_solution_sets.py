"""Renderer-independent mathematics for CP113.

Checkpoint 113 classifies the solution set of a linear system directly from
its reduced row echelon augmented matrix.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
Classification = Literal["unique", "none", "infinite"]


@dataclass(frozen=True)
class RREFSolutionCase:
    """One RREF example and its solution-set interpretation."""

    name: str
    augmented: FloatArray
    classification: Classification
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    contradiction_row: int | None
    interpretation_tex: tuple[str, ...]


@dataclass(frozen=True)
class RREFSolutionSetsSnapshot:
    """Immutable data used by the CP113 presentation."""

    cases: tuple[RREFSolutionCase, ...]


class RREFSolutionSets:
    """Provide and classify the three fundamental RREF outcomes."""

    UNIQUE = np.array(
        [
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 1.0, 0.0, -1.0],
            [0.0, 0.0, 1.0, 3.0],
        ],
        dtype=float,
    )

    NONE = np.array(
        [
            [1.0, 0.0, 2.0, 4.0],
            [0.0, 1.0, -1.0, 1.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )

    INFINITE = np.array(
        [
            [1.0, 0.0, 2.0, 4.0],
            [0.0, 1.0, -1.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    def classify(self, augmented: Iterable[Iterable[float]] | FloatArray) -> Classification:
        matrix = self._coerce(augmented)
        coefficient_block = matrix[:, :-1]
        rhs = matrix[:, -1]

        zero_left = np.all(np.isclose(coefficient_block, 0.0), axis=1)
        inconsistent = np.any(zero_left & ~np.isclose(rhs, 0.0))
        if inconsistent:
            return "none"

        pivots = self.pivot_columns(matrix)
        variable_count = coefficient_block.shape[1]
        if len(pivots) == variable_count:
            return "unique"
        return "infinite"

    def pivot_columns(self, augmented: Iterable[Iterable[float]] | FloatArray) -> tuple[int, ...]:
        matrix = self._coerce(augmented)
        pivots: list[int] = []
        for row in matrix[:, :-1]:
            nonzero = np.flatnonzero(~np.isclose(row, 0.0))
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    def free_columns(self, augmented: Iterable[Iterable[float]] | FloatArray) -> tuple[int, ...]:
        matrix = self._coerce(augmented)
        pivots = set(self.pivot_columns(matrix))
        return tuple(column for column in range(matrix.shape[1] - 1) if column not in pivots)

    def contradiction_row(self, augmented: Iterable[Iterable[float]] | FloatArray) -> int | None:
        matrix = self._coerce(augmented)
        coefficient_block = matrix[:, :-1]
        rhs = matrix[:, -1]
        for index, (row, value) in enumerate(zip(coefficient_block, rhs, strict=True)):
            if np.all(np.isclose(row, 0.0)) and not np.isclose(value, 0.0):
                return index
        return None

    def case(self, name: str, augmented: FloatArray, interpretation_tex: tuple[str, ...]) -> RREFSolutionCase:
        classification = self.classify(augmented)
        return RREFSolutionCase(
            name=name,
            augmented=np.array(augmented, dtype=float, copy=True),
            classification=classification,
            pivot_columns=self.pivot_columns(augmented),
            free_columns=self.free_columns(augmented),
            contradiction_row=self.contradiction_row(augmented),
            interpretation_tex=interpretation_tex,
        )

    def cases(self) -> tuple[RREFSolutionCase, ...]:
        return (
            self.case(
                "Unique solution",
                self.UNIQUE,
                (r"x=2", r"y=-1", r"z=3"),
            ),
            self.case(
                "No solution",
                self.NONE,
                (r"0=1", r"\text{impossible}"),
            ),
            self.case(
                "Infinitely many solutions",
                self.INFINITE,
                (r"z=t", r"x=4-2t", r"y=1+t"),
            ),
        )

    def snapshot(self) -> RREFSolutionSetsSnapshot:
        return RREFSolutionSetsSnapshot(cases=self.cases())

    @staticmethod
    def _coerce(augmented: Iterable[Iterable[float]] | FloatArray) -> FloatArray:
        matrix = np.array(augmented, dtype=float, copy=True)
        if matrix.ndim != 2:
            raise ValueError("augmented matrix must be two-dimensional.")
        if matrix.shape[1] < 2:
            raise ValueError("augmented matrix must contain variables and a right-hand side.")
        if not np.isfinite(matrix).all():
            raise ValueError("augmented matrix entries must be finite.")
        return matrix
