"""Renderer-independent mathematics for CP109.

Checkpoint 109 performs Gaussian elimination on a full-rank 3 by 3 system and
records every augmented-matrix stage on the way to row echelon form.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class EliminationOperation:
    """One elementary row operation in the elimination sequence."""

    label: str
    kind: str
    target: int
    source: int | None = None
    scalar: float | None = None


@dataclass(frozen=True)
class GaussianEliminationSnapshot:
    """Immutable data used by the CP109 presentation."""

    stages: tuple[FloatArray, ...]
    operations: tuple[EliminationOperation, ...]
    pivot_positions: tuple[tuple[int, int], ...]
    solution: FloatArray

    @property
    def original_augmented(self) -> FloatArray:
        return self.stages[0].copy()

    @property
    def echelon_augmented(self) -> FloatArray:
        return self.stages[-1].copy()


class GaussianEliminationToEchelon:
    """Carry one 3 by 3 augmented system to row echelon form."""

    DEFAULT_AUGMENTED = np.array(
        [
            [1.0, 1.0, 1.0, 3.0],
            [2.0, -1.0, 1.0, 2.0],
            [1.0, 2.0, -1.0, 2.0],
        ],
        dtype=float,
    )

    OPERATIONS = (
        EliminationOperation(
            label=r"R_2\leftarrow R_2-2R_1",
            kind="replace",
            target=1,
            source=0,
            scalar=-2.0,
        ),
        EliminationOperation(
            label=r"R_3\leftarrow R_3-R_1",
            kind="replace",
            target=2,
            source=0,
            scalar=-1.0,
        ),
        EliminationOperation(
            label=r"R_2\leftrightarrow R_3",
            kind="swap",
            target=1,
            source=2,
        ),
        EliminationOperation(
            label=r"R_3\leftarrow R_3+3R_2",
            kind="replace",
            target=2,
            source=1,
            scalar=3.0,
        ),
    )

    def __init__(
        self,
        augmented_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
    ) -> None:
        candidate = np.array(
            self.DEFAULT_AUGMENTED if augmented_matrix is None else augmented_matrix,
            dtype=float,
            copy=True,
        )
        self._validate_augmented(candidate)
        if candidate.shape != (3, 4):
            raise ValueError("the CP109 demonstration requires a 3 by 4 augmented matrix.")
        if np.linalg.matrix_rank(candidate[:, :-1]) != 3:
            raise ValueError("the CP109 demonstration requires a full-rank system.")
        self._augmented = candidate

    @property
    def augmented_matrix(self) -> FloatArray:
        return self._augmented.copy()

    def stages(self) -> tuple[FloatArray, ...]:
        current = self.augmented_matrix
        result: list[FloatArray] = [current.copy()]
        for operation in self.OPERATIONS:
            if operation.kind == "replace":
                assert operation.source is not None
                assert operation.scalar is not None
                current = self.replace_row(
                    current,
                    target=operation.target,
                    source=operation.source,
                    scalar=operation.scalar,
                )
            elif operation.kind == "swap":
                assert operation.source is not None
                current = self.swap_rows(
                    current,
                    first=operation.target,
                    second=operation.source,
                )
            else:  # pragma: no cover - operations are a class constant
                raise ValueError(f"unsupported operation kind: {operation.kind}")
            result.append(current.copy())
        return tuple(result)

    def echelon_augmented(self) -> FloatArray:
        return self.stages()[-1].copy()

    def pivot_positions(
        self,
        augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        atol: float = 1e-9,
    ) -> tuple[tuple[int, int], ...]:
        matrix = self._coerce_augmented(
            self.echelon_augmented() if augmented is None else augmented
        )
        coefficient_block = matrix[:, :-1]
        pivots: list[tuple[int, int]] = []
        for row_index, row in enumerate(coefficient_block):
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append((row_index, int(nonzero[0])))
        return tuple(pivots)

    def is_row_echelon(
        self,
        augmented: Iterable[Iterable[float]] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        matrix = self._coerce_augmented(augmented)
        coefficient_block = matrix[:, :-1]
        previous_pivot = -1
        encountered_zero_row = False
        for row in coefficient_block:
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size == 0:
                encountered_zero_row = True
                continue
            if encountered_zero_row:
                return False
            pivot = int(nonzero[0])
            if pivot <= previous_pivot:
                return False
            previous_pivot = pivot
        for row_index, pivot_column in self._pivot_positions_for_matrix(
            coefficient_block,
            atol=atol,
        ):
            if np.any(np.abs(coefficient_block[row_index + 1 :, pivot_column]) > atol):
                return False
        return True

    def solution(self) -> FloatArray:
        return np.linalg.solve(self._augmented[:, :-1], self._augmented[:, -1])

    def snapshot(self) -> GaussianEliminationSnapshot:
        stages = self.stages()
        return GaussianEliminationSnapshot(
            stages=stages,
            operations=self.OPERATIONS,
            pivot_positions=self.pivot_positions(stages[-1]),
            solution=self.solution(),
        )

    @classmethod
    def replace_row(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        *,
        target: int,
        source: int,
        scalar: float,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, target)
        cls._validate_row_index(result, source)
        if target == source:
            raise ValueError("row replacement requires distinct source and target rows.")
        if not np.isfinite(scalar):
            raise ValueError("row replacement scalar must be finite.")
        result[target] = result[target] + float(scalar) * result[source]
        return result

    @classmethod
    def swap_rows(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        *,
        first: int,
        second: int,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, first)
        cls._validate_row_index(result, second)
        if first == second:
            raise ValueError("row swap requires distinct rows.")
        result[[first, second]] = result[[second, first]]
        return result

    @classmethod
    def _coerce_augmented(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
    ) -> FloatArray:
        result = np.array(augmented, dtype=float, copy=True)
        cls._validate_augmented(result)
        return result

    @staticmethod
    def _validate_augmented(candidate: FloatArray) -> None:
        if candidate.ndim != 2:
            raise ValueError("augmented matrix must be two-dimensional.")
        if candidate.shape[0] == 0 or candidate.shape[1] < 2:
            raise ValueError("augmented matrix must contain rows and variables.")
        if not np.isfinite(candidate).all():
            raise ValueError("augmented entries must be finite.")

    @staticmethod
    def _validate_row_index(candidate: FloatArray, row: int) -> None:
        if not isinstance(row, (int, np.integer)):
            raise TypeError("row index must be an integer.")
        if not 0 <= int(row) < candidate.shape[0]:
            raise IndexError("row index is outside the augmented matrix.")

    @staticmethod
    def _pivot_positions_for_matrix(
        coefficient_block: FloatArray,
        *,
        atol: float,
    ) -> tuple[tuple[int, int], ...]:
        pivots: list[tuple[int, int]] = []
        for row_index, row in enumerate(coefficient_block):
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append((row_index, int(nonzero[0])))
        return tuple(pivots)
