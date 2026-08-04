"""Renderer-independent data for encoding equations as an augmented matrix.

Checkpoint 106 preserves the same three-equation system used in CP105 and
records exactly which information survives when variable names and equality
signs are suppressed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class AugmentedMatrixSnapshot:
    """Immutable data for one system and its augmented representation."""

    coefficient_matrix: FloatArray
    right_hand_side: FloatArray
    augmented_matrix: FloatArray
    variable_names: tuple[str, ...]
    natural_equation_tex: tuple[str, ...]
    explicit_equation_tex: tuple[str, ...]


class AugmentedMatrixEncoding:
    """Encode a linear system while preserving coefficient-column order.

    The default system is

    ``x + y + z = 3``
    ``2x - y + z = 2``
    ``x + 2y - z = 2``

    and the variable order is ``(x, y, z)``.
    """

    DEFAULT_MATRIX = np.array(
        [
            [1.0, 1.0, 1.0],
            [2.0, -1.0, 1.0],
            [1.0, 2.0, -1.0],
        ],
        dtype=float,
    )
    DEFAULT_RIGHT_HAND_SIDE = np.array([3.0, 2.0, 2.0], dtype=float)
    DEFAULT_VARIABLES = ("x", "y", "z")

    def __init__(
        self,
        coefficient_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        right_hand_side: Iterable[float] | FloatArray | None = None,
        variable_names: Sequence[str] | None = None,
    ) -> None:
        matrix = np.array(
            self.DEFAULT_MATRIX if coefficient_matrix is None else coefficient_matrix,
            dtype=float,
            copy=True,
        )
        rhs = np.array(
            self.DEFAULT_RIGHT_HAND_SIDE
            if right_hand_side is None
            else right_hand_side,
            dtype=float,
            copy=True,
        )
        variables = tuple(
            self.DEFAULT_VARIABLES if variable_names is None else variable_names
        )

        if matrix.ndim != 2:
            raise ValueError("coefficient_matrix must be two-dimensional.")
        if matrix.shape[0] == 0 or matrix.shape[1] == 0:
            raise ValueError("coefficient_matrix must be nonempty.")
        if rhs.shape != (matrix.shape[0],):
            raise ValueError(
                "right_hand_side length must equal the number of equations."
            )
        if len(variables) != matrix.shape[1]:
            raise ValueError(
                "variable_names length must equal the number of coefficient columns."
            )
        if any(not isinstance(name, str) or not name.strip() for name in variables):
            raise ValueError("variable names must be nonempty strings.")
        if len(set(variables)) != len(variables):
            raise ValueError("variable names must be unique.")
        if not np.isfinite(matrix).all():
            raise ValueError("coefficient entries must be finite.")
        if not np.isfinite(rhs).all():
            raise ValueError("right-hand-side entries must be finite.")

        self._matrix = matrix
        self._rhs = rhs
        self._variables = variables

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def right_hand_side(self) -> FloatArray:
        return self._rhs.copy()

    @property
    def variable_names(self) -> tuple[str, ...]:
        return self._variables

    @property
    def augmented_matrix(self) -> FloatArray:
        return np.column_stack((self._matrix, self._rhs))

    def snapshot(self) -> AugmentedMatrixSnapshot:
        return AugmentedMatrixSnapshot(
            coefficient_matrix=self.coefficient_matrix,
            right_hand_side=self.right_hand_side,
            augmented_matrix=self.augmented_matrix,
            variable_names=self.variable_names,
            natural_equation_tex=tuple(
                self._format_equation(row, target, explicit=False)
                for row, target in zip(self._matrix, self._rhs, strict=True)
            ),
            explicit_equation_tex=tuple(
                self._format_equation(row, target, explicit=True)
                for row, target in zip(self._matrix, self._rhs, strict=True)
            ),
        )

    def augmented_row(self, row_index: int) -> FloatArray:
        if not 0 <= row_index < self._matrix.shape[0]:
            raise IndexError("row_index is outside the system.")
        return self.augmented_matrix[row_index].copy()

    def column_for(self, variable_name: str) -> FloatArray:
        try:
            index = self._variables.index(variable_name)
        except ValueError as exc:
            raise KeyError(f"unknown variable: {variable_name}") from exc
        return self._matrix[:, index].copy()

    @staticmethod
    def split_augmented(augmented: Iterable[Iterable[float]] | FloatArray) -> tuple[FloatArray, FloatArray]:
        candidate = np.array(augmented, dtype=float, copy=True)
        if candidate.ndim != 2 or candidate.shape[1] < 2:
            raise ValueError("augmented matrix must have at least two columns.")
        if not np.isfinite(candidate).all():
            raise ValueError("augmented entries must be finite.")
        return candidate[:, :-1].copy(), candidate[:, -1].copy()

    @staticmethod
    def encode_row(
        coefficients: Iterable[float] | FloatArray,
        right_hand_side: float,
    ) -> FloatArray:
        row = np.array(coefficients, dtype=float, copy=True)
        if row.ndim != 1 or row.size == 0:
            raise ValueError("coefficients must be a nonempty one-dimensional row.")
        if not np.isfinite(row).all() or not np.isfinite(right_hand_side):
            raise ValueError("row entries must be finite.")
        return np.concatenate((row, np.array([float(right_hand_side)])))

    def _format_equation(
        self,
        row: FloatArray,
        target: float,
        *,
        explicit: bool,
    ) -> str:
        if explicit:
            terms = [
                f"{self._signed_parenthesized(coefficient)}{variable}"
                for coefficient, variable in zip(row, self._variables, strict=True)
            ]
            left = "+".join(terms)
            return f"{left}={self._number_tex(target)}"

        terms: list[str] = []
        for coefficient, variable in zip(row, self._variables, strict=True):
            if np.isclose(coefficient, 0.0):
                continue
            magnitude = abs(float(coefficient))
            coefficient_tex = "" if np.isclose(magnitude, 1.0) else self._number_tex(magnitude)
            term = f"{coefficient_tex}{variable}"
            if not terms:
                terms.append(f"-{term}" if coefficient < 0 else term)
            else:
                terms.append(("-" if coefficient < 0 else "+") + term)
        left = "".join(terms) if terms else "0"
        return f"{left}={self._number_tex(target)}"

    @classmethod
    def _signed_parenthesized(cls, value: float) -> str:
        number = cls._number_tex(value)
        return f"({number})" if value < 0 else number

    @staticmethod
    def _number_tex(value: float) -> str:
        rounded = int(round(float(value)))
        if np.isclose(value, rounded):
            return str(rounded)
        return f"{float(value):g}"
