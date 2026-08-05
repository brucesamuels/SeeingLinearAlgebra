"""Renderer-independent mathematics for CP118.

Checkpoint 118 connects pivots and rank with consistency and the number of
solutions of a linear system in reduced row-echelon form.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RankConsistencyCase:
    """Immutable rank data for one augmented system in RREF."""

    name: str
    rref_augmented: FloatArray
    coefficient_rank: int
    augmented_rank: int
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    variable_count: int
    is_consistent: bool
    solution_type: str
    reason: str


@dataclass(frozen=True)
class RankPivotsConsistencySnapshot:
    """All mathematical data needed by the CP118 presentation."""

    unique: RankConsistencyCase
    infinite: RankConsistencyCase
    inconsistent: RankConsistencyCase
    consistency_theorem_tex: tuple[str, ...]
    classification_tex: tuple[str, ...]


class RankPivotsConsistency:
    """Classify RREF systems by coefficient and augmented rank."""

    DEFAULT_CASES = {
        "unique": np.array(
            [
                [1.0, 0.0, 0.0, 2.0],
                [0.0, 1.0, 0.0, -1.0],
                [0.0, 0.0, 1.0, 3.0],
            ],
            dtype=float,
        ),
        "infinite": np.array(
            [
                [1.0, 0.0, 2.0, 4.0],
                [0.0, 1.0, -1.0, 1.0],
                [0.0, 0.0, 0.0, 0.0],
            ],
            dtype=float,
        ),
        "inconsistent": np.array(
            [
                [1.0, 0.0, 2.0, 4.0],
                [0.0, 1.0, -1.0, 1.0],
                [0.0, 0.0, 0.0, 3.0],
            ],
            dtype=float,
        ),
    }

    def __init__(
        self,
        cases: dict[str, Iterable[Iterable[float]] | FloatArray] | None = None,
        *,
        atol: float = 1e-9,
    ) -> None:
        if not np.isfinite(atol) or atol <= 0:
            raise ValueError("atol must be a positive finite number.")
        source = self.DEFAULT_CASES if cases is None else cases
        required = {"unique", "infinite", "inconsistent"}
        if set(source) != required:
            raise ValueError("cases must contain unique, infinite, and inconsistent systems.")

        prepared: dict[str, FloatArray] = {}
        for name, values in source.items():
            matrix = np.array(values, dtype=float, copy=True)
            if matrix.shape != (3, 4):
                raise ValueError(f"{name} augmented matrix must have shape (3, 4).")
            if not np.isfinite(matrix).all():
                raise ValueError(f"{name} augmented matrix entries must be finite.")
            prepared[name] = matrix
        self._cases = prepared
        self._atol = float(atol)

    @staticmethod
    def _row_rank(matrix: FloatArray, *, atol: float) -> int:
        """Count nonzero rows of a matrix already in row-echelon form."""
        return int(np.count_nonzero(np.any(np.abs(matrix) > atol, axis=1)))

    @staticmethod
    def _pivot_columns(coefficient: FloatArray, *, atol: float) -> tuple[int, ...]:
        pivots: list[int] = []
        for row in coefficient:
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    def case(self, name: str) -> RankConsistencyCase:
        if name not in self._cases:
            raise KeyError(f"unknown case: {name}")

        augmented = self._cases[name].copy()
        coefficient = augmented[:, :-1]
        coefficient_rank = self._row_rank(coefficient, atol=self._atol)
        augmented_rank = self._row_rank(augmented, atol=self._atol)
        pivot_columns = self._pivot_columns(coefficient, atol=self._atol)
        variable_count = coefficient.shape[1]
        free_columns = tuple(index for index in range(variable_count) if index not in pivot_columns)
        is_consistent = coefficient_rank == augmented_rank

        if not is_consistent:
            solution_type = "none"
            reason = "The augmented column creates an additional pivot."
        elif coefficient_rank == variable_count:
            solution_type = "unique"
            reason = "Every variable column contains a pivot."
        else:
            solution_type = "infinite"
            reason = "At least one variable is free."

        return RankConsistencyCase(
            name=name,
            rref_augmented=augmented,
            coefficient_rank=coefficient_rank,
            augmented_rank=augmented_rank,
            pivot_columns=pivot_columns,
            free_columns=free_columns,
            variable_count=variable_count,
            is_consistent=is_consistent,
            solution_type=solution_type,
            reason=reason,
        )

    def snapshot(self) -> RankPivotsConsistencySnapshot:
        return RankPivotsConsistencySnapshot(
            unique=self.case("unique"),
            infinite=self.case("infinite"),
            inconsistent=self.case("inconsistent"),
            consistency_theorem_tex=(
                r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])",
                r"\operatorname{rank}(A)<\operatorname{rank}([A\mid\mathbf{b}])",
            ),
            classification_tex=(
                r"\operatorname{rank}(A)=n\ \Longrightarrow\ \text{unique solution}",
                r"\operatorname{rank}(A)<n\ \Longrightarrow\ \text{free variables}",
            ),
        )
