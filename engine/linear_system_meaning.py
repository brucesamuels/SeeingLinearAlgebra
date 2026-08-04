"""Renderer-independent mathematics for introducing ``A x = b``.

Checkpoint 105 deliberately models the meaning of a linear system without
performing row reduction. The lesson now begins with a two-dimensional system
whose solution is the intersection of two lines, then scaffolds upward to a
three-dimensional system whose solution is the common point of three planes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class PlanarLinearSystemSnapshot:
    """Immutable lesson data for the 2 by 2 opening example."""

    matrix: FloatArray
    right_hand_side: FloatArray
    solution: FloatArray
    determinant: float
    equation_tex: tuple[str, str]


@dataclass(frozen=True)
class LinearSystemMeaningSnapshot:
    """Immutable lesson data derived from one nonsingular 3 by 3 system."""

    matrix: FloatArray
    right_hand_side: FloatArray
    solution: FloatArray
    columns: FloatArray
    weighted_columns: FloatArray
    reconstructed_right_hand_side: FloatArray
    determinant: float
    equation_tex: tuple[str, str, str]


class LinearSystemMeaning:
    """Represent one 2D opening system and one uniquely solvable 3D system.

    The opening planar system is

    ``x + y = 2``
    ``x - y = 0``

    whose two lines meet at ``(1, 1)``.

    The main three-dimensional system is

    ``x + y + z = 3``
    ``2x - y + z = 2``
    ``x + 2y - z = 2``

    whose three planes meet at ``(1, 1, 1)``.
    """

    DEFAULT_2D_MATRIX = np.array(
        [
            [1.0, 1.0],
            [1.0, -1.0],
        ],
        dtype=float,
    )
    DEFAULT_2D_RIGHT_HAND_SIDE = np.array([2.0, 0.0], dtype=float)

    DEFAULT_MATRIX = np.array(
        [
            [1.0, 1.0, 1.0],
            [2.0, -1.0, 1.0],
            [1.0, 2.0, -1.0],
        ],
        dtype=float,
    )
    DEFAULT_RIGHT_HAND_SIDE = np.array([3.0, 2.0, 2.0], dtype=float)

    def __init__(
        self,
        matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        right_hand_side: Iterable[float] | FloatArray | None = None,
        matrix_2d: Iterable[Iterable[float]] | FloatArray | None = None,
        right_hand_side_2d: Iterable[float] | FloatArray | None = None,
    ) -> None:
        candidate_matrix = np.array(
            self.DEFAULT_MATRIX if matrix is None else matrix,
            dtype=float,
            copy=True,
        )
        candidate_rhs = np.array(
            self.DEFAULT_RIGHT_HAND_SIDE
            if right_hand_side is None
            else right_hand_side,
            dtype=float,
            copy=True,
        )
        candidate_matrix_2d = np.array(
            self.DEFAULT_2D_MATRIX if matrix_2d is None else matrix_2d,
            dtype=float,
            copy=True,
        )
        candidate_rhs_2d = np.array(
            self.DEFAULT_2D_RIGHT_HAND_SIDE
            if right_hand_side_2d is None
            else right_hand_side_2d,
            dtype=float,
            copy=True,
        )

        if candidate_matrix.shape != (3, 3):
            raise ValueError("matrix must have shape (3, 3).")
        if candidate_rhs.shape != (3,):
            raise ValueError("right_hand_side must have shape (3,).")
        if candidate_matrix_2d.shape != (2, 2):
            raise ValueError("matrix_2d must have shape (2, 2).")
        if candidate_rhs_2d.shape != (2,):
            raise ValueError("right_hand_side_2d must have shape (2,).")
        if not np.isfinite(candidate_matrix).all():
            raise ValueError("matrix entries must be finite.")
        if not np.isfinite(candidate_rhs).all():
            raise ValueError("right_hand_side entries must be finite.")
        if not np.isfinite(candidate_matrix_2d).all():
            raise ValueError("matrix_2d entries must be finite.")
        if not np.isfinite(candidate_rhs_2d).all():
            raise ValueError("right_hand_side_2d entries must be finite.")
        if np.linalg.matrix_rank(candidate_matrix) != 3:
            raise ValueError("matrix must have a unique solution.")
        if np.linalg.matrix_rank(candidate_matrix_2d) != 2:
            raise ValueError("matrix_2d must have a unique solution.")
        if np.any(np.isclose(candidate_matrix[:, 2], 0.0)):
            raise ValueError(
                "each default lesson plane must be expressible as z=f(x,y)."
            )
        if np.any(np.isclose(candidate_matrix_2d[:, 1], 0.0)):
            raise ValueError(
                "each default lesson line must be expressible as y=f(x)."
            )

        self._matrix = candidate_matrix
        self._right_hand_side = candidate_rhs
        self._matrix_2d = candidate_matrix_2d
        self._right_hand_side_2d = candidate_rhs_2d

    @property
    def matrix(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def right_hand_side(self) -> FloatArray:
        return self._right_hand_side.copy()

    @property
    def matrix_2d(self) -> FloatArray:
        return self._matrix_2d.copy()

    @property
    def right_hand_side_2d(self) -> FloatArray:
        return self._right_hand_side_2d.copy()

    def planar_snapshot(self) -> PlanarLinearSystemSnapshot:
        solution = np.linalg.solve(self._matrix_2d, self._right_hand_side_2d)
        return PlanarLinearSystemSnapshot(
            matrix=self._matrix_2d.copy(),
            right_hand_side=self._right_hand_side_2d.copy(),
            solution=solution.copy(),
            determinant=float(np.linalg.det(self._matrix_2d)),
            equation_tex=self._equation_tex_2d(),
        )

    def snapshot(self) -> LinearSystemMeaningSnapshot:
        solution = np.linalg.solve(self._matrix, self._right_hand_side)
        columns = self._matrix.T.copy()
        weighted_columns = columns * solution[:, np.newaxis]
        reconstructed = weighted_columns.sum(axis=0)

        return LinearSystemMeaningSnapshot(
            matrix=self._matrix.copy(),
            right_hand_side=self._right_hand_side.copy(),
            solution=solution.copy(),
            columns=columns,
            weighted_columns=weighted_columns,
            reconstructed_right_hand_side=reconstructed,
            determinant=float(np.linalg.det(self._matrix)),
            equation_tex=self._equation_tex(),
        )

    def line_height(self, row_index: int, x: float) -> float:
        """Return the y-coordinate on one equation's line."""

        if row_index not in (0, 1):
            raise IndexError("row_index must be 0 or 1.")
        a, b = self._matrix_2d[row_index]
        rhs = self._right_hand_side_2d[row_index]
        return float((rhs - a * float(x)) / b)

    def plane_height(self, row_index: int, x: float, y: float) -> float:
        """Return the z-coordinate on one equation's plane."""

        if row_index not in (0, 1, 2):
            raise IndexError("row_index must be 0, 1, or 2.")
        a, b, c = self._matrix[row_index]
        rhs = self._right_hand_side[row_index]
        return float((rhs - a * float(x) - b * float(y)) / c)

    def residual(self, point: Iterable[float] | FloatArray) -> FloatArray:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        if not np.isfinite(candidate).all():
            raise ValueError("point entries must be finite.")
        return self._matrix @ candidate - self._right_hand_side

    def planar_residual(self, point: Iterable[float] | FloatArray) -> FloatArray:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (2,):
            raise ValueError("point must have shape (2,).")
        if not np.isfinite(candidate).all():
            raise ValueError("point entries must be finite.")
        return self._matrix_2d @ candidate - self._right_hand_side_2d

    def satisfies(self, point: Iterable[float] | FloatArray, tol: float = 1e-9) -> bool:
        if not np.isfinite(tol) or tol < 0:
            raise ValueError("tol must be finite and nonnegative.")
        return bool(np.all(np.abs(self.residual(point)) <= tol))

    def planar_satisfies(
        self,
        point: Iterable[float] | FloatArray,
        tol: float = 1e-9,
    ) -> bool:
        if not np.isfinite(tol) or tol < 0:
            raise ValueError("tol must be finite and nonnegative.")
        return bool(np.all(np.abs(self.planar_residual(point)) <= tol))

    def _equation_tex(self) -> tuple[str, str, str]:
        return self._format_equations(self._matrix, self._right_hand_side, ("x", "y", "z"))  # type: ignore[return-value]

    def _equation_tex_2d(self) -> tuple[str, str]:
        return self._format_equations(self._matrix_2d, self._right_hand_side_2d, ("x", "y"))  # type: ignore[return-value]

    @staticmethod
    def _format_equations(
        matrix: FloatArray,
        rhs: FloatArray,
        variables: tuple[str, ...],
    ) -> tuple[str, ...]:
        equations: list[str] = []
        for row, target in zip(matrix, rhs, strict=True):
            terms: list[str] = []
            for coefficient, variable in zip(row, variables, strict=True):
                rounded = int(round(float(coefficient)))
                if np.isclose(coefficient, rounded):
                    value: float | int = rounded
                else:
                    value = float(coefficient)
                if np.isclose(value, 0.0):
                    continue
                magnitude = abs(value)
                coefficient_text = "" if np.isclose(magnitude, 1.0) else f"{magnitude:g}"
                term = f"{coefficient_text}{variable}"
                if not terms:
                    terms.append(term if value > 0 else f"-{term}")
                else:
                    terms.append(("+" if value > 0 else "-") + term)
            equations.append("".join(terms) + f"={float(target):g}")
        return tuple(equations)
