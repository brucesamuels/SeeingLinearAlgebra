"""Renderer-independent Gaussian elimination algorithm for CP111."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class EliminationAction:
    """One row operation performed by Gaussian elimination."""

    kind: str
    label: str
    pivot_row: int
    pivot_column: int
    target_row: int
    source_row: int
    scalar: float | None
    result: FloatArray


@dataclass(frozen=True)
class EliminationAlgorithmSnapshot:
    """Immutable trace consumed by the CP111 presentation."""

    original_augmented: FloatArray
    actions: tuple[EliminationAction, ...]
    pivot_positions: tuple[tuple[int, int], ...]
    active_regions: tuple[tuple[int, int], ...]
    echelon_augmented: FloatArray


class EliminationAlgorithm:
    """Trace the standard left-to-right Gaussian elimination procedure."""

    DEFAULT_AUGMENTED = np.array(
        [
            [0.0, 1.0, 1.0, 2.0],
            [1.0, 1.0, 1.0, 3.0],
            [2.0, 3.0, 1.0, 6.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        augmented_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        atol: float = 1e-9,
    ) -> None:
        matrix = np.array(
            self.DEFAULT_AUGMENTED if augmented_matrix is None else augmented_matrix,
            dtype=float,
            copy=True,
        )
        self._validate_augmented(matrix)
        if atol < 0 or not np.isfinite(atol):
            raise ValueError("atol must be finite and nonnegative.")
        self._augmented = matrix
        self._atol = float(atol)

    @property
    def augmented_matrix(self) -> FloatArray:
        return self._augmented.copy()

    def snapshot(self) -> EliminationAlgorithmSnapshot:
        current = self.augmented_matrix
        coefficient_columns = current.shape[1] - 1
        pivot_row = 0
        pivots: list[tuple[int, int]] = []
        active_regions: list[tuple[int, int]] = []
        actions: list[EliminationAction] = []

        for pivot_column in range(coefficient_columns):
            if pivot_row >= current.shape[0]:
                break

            candidates = np.flatnonzero(
                np.abs(current[pivot_row:, pivot_column]) > self._atol
            )
            if candidates.size == 0:
                continue

            active_regions.append((pivot_row, pivot_column))
            selected_row = pivot_row + int(candidates[0])
            if selected_row != pivot_row:
                current = self.swap_rows(current, pivot_row, selected_row)
                actions.append(
                    EliminationAction(
                        kind="swap",
                        label=rf"R_{pivot_row + 1}\leftrightarrow R_{selected_row + 1}",
                        pivot_row=pivot_row,
                        pivot_column=pivot_column,
                        target_row=pivot_row,
                        source_row=selected_row,
                        scalar=None,
                        result=current.copy(),
                    )
                )

            pivot_value = current[pivot_row, pivot_column]
            for target_row in range(pivot_row + 1, current.shape[0]):
                entry = current[target_row, pivot_column]
                if abs(entry) <= self._atol:
                    continue
                factor = entry / pivot_value
                current = self.replace_row(
                    current,
                    target=target_row,
                    source=pivot_row,
                    scalar=-factor,
                )
                actions.append(
                    EliminationAction(
                        kind="replace",
                        label=self._replacement_label(
                            target_row=target_row,
                            source_row=pivot_row,
                            factor=factor,
                        ),
                        pivot_row=pivot_row,
                        pivot_column=pivot_column,
                        target_row=target_row,
                        source_row=pivot_row,
                        scalar=-float(factor),
                        result=current.copy(),
                    )
                )

            pivots.append((pivot_row, pivot_column))
            pivot_row += 1

        return EliminationAlgorithmSnapshot(
            original_augmented=self.augmented_matrix,
            actions=tuple(actions),
            pivot_positions=tuple(pivots),
            active_regions=tuple(active_regions),
            echelon_augmented=current.copy(),
        )

    def is_row_echelon(
        self,
        augmented_matrix: Iterable[Iterable[float]] | FloatArray,
    ) -> bool:
        matrix = np.array(augmented_matrix, dtype=float, copy=True)
        self._validate_augmented(matrix)
        coefficients = matrix[:, :-1]
        previous_pivot = -1
        zero_row_seen = False
        for row_index, row in enumerate(coefficients):
            nonzero = np.flatnonzero(np.abs(row) > self._atol)
            if nonzero.size == 0:
                zero_row_seen = True
                continue
            if zero_row_seen:
                return False
            pivot_column = int(nonzero[0])
            if pivot_column <= previous_pivot:
                return False
            if np.any(np.abs(coefficients[row_index + 1 :, pivot_column]) > self._atol):
                return False
            previous_pivot = pivot_column
        return True

    @staticmethod
    def swap_rows(matrix: FloatArray, first: int, second: int) -> FloatArray:
        result = np.array(matrix, dtype=float, copy=True)
        if first == second:
            return result
        result[[first, second]] = result[[second, first]]
        return result

    @staticmethod
    def replace_row(
        matrix: FloatArray,
        *,
        target: int,
        source: int,
        scalar: float,
    ) -> FloatArray:
        result = np.array(matrix, dtype=float, copy=True)
        if target == source:
            raise ValueError("source and target rows must be distinct.")
        if not np.isfinite(scalar):
            raise ValueError("row replacement scalar must be finite.")
        result[target] = result[target] + float(scalar) * result[source]
        return result

    @staticmethod
    def _replacement_label(*, target_row: int, source_row: int, factor: float) -> str:
        magnitude = abs(float(factor))
        if abs(magnitude - round(magnitude)) < 1e-9:
            factor_text = str(int(round(magnitude)))
        else:
            factor_text = f"{magnitude:g}"
        coefficient = "" if factor_text == "1" else factor_text
        sign = "-" if factor > 0 else "+"
        return (
            rf"R_{target_row + 1}\leftarrow "
            rf"R_{target_row + 1}{sign}{coefficient}R_{source_row + 1}"
        )

    @staticmethod
    def _validate_augmented(matrix: FloatArray) -> None:
        if matrix.ndim != 2:
            raise ValueError("the augmented matrix must be two-dimensional.")
        if matrix.shape[0] == 0 or matrix.shape[1] < 2:
            raise ValueError("the augmented matrix must contain rows and a right-hand side.")
        if not np.isfinite(matrix).all():
            raise ValueError("the augmented matrix must contain finite entries.")
