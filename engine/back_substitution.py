"""Renderer-independent mathematics for CP110.

Checkpoint 110 begins with the row echelon form produced in CP109 and solves
for the variables by back substitution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class BackSubstitutionStep:
    """One algebraic step in the back-substitution sequence."""

    variable: str
    equation_tex: str
    solved_tex: str
    value: float


@dataclass(frozen=True)
class BackSubstitutionSnapshot:
    """Immutable data used by the CP110 presentation."""

    echelon_augmented: FloatArray
    original_augmented: FloatArray
    steps: tuple[BackSubstitutionStep, ...]
    solution: FloatArray
    original_equations_tex: tuple[str, str, str]


class BackSubstitution:
    """Solve the CP109 echelon system by working upward."""

    DEFAULT_ECHELON_AUGMENTED = np.array(
        [
            [1.0, 1.0, 1.0, 3.0],
            [0.0, 1.0, -2.0, -1.0],
            [0.0, 0.0, -7.0, -7.0],
        ],
        dtype=float,
    )

    DEFAULT_ORIGINAL_AUGMENTED = np.array(
        [
            [1.0, 1.0, 1.0, 3.0],
            [2.0, -1.0, 1.0, 2.0],
            [1.0, 2.0, -1.0, 2.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        echelon_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        original_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
    ) -> None:
        echelon = np.array(
            self.DEFAULT_ECHELON_AUGMENTED if echelon_augmented is None else echelon_augmented,
            dtype=float,
            copy=True,
        )
        original = np.array(
            self.DEFAULT_ORIGINAL_AUGMENTED if original_augmented is None else original_augmented,
            dtype=float,
            copy=True,
        )
        self._validate_augmented(echelon)
        self._validate_augmented(original)
        if echelon.shape != (3, 4):
            raise ValueError("echelon_augmented must have shape (3, 4).")
        if original.shape != (3, 4):
            raise ValueError("original_augmented must have shape (3, 4).")
        if np.linalg.matrix_rank(echelon[:, :-1]) != 3:
            raise ValueError("the echelon matrix must be full rank.")
        if np.linalg.matrix_rank(original[:, :-1]) != 3:
            raise ValueError("the original system must be full rank.")
        self._echelon = echelon
        self._original = original

    @property
    def echelon_augmented(self) -> FloatArray:
        return self._echelon.copy()

    @property
    def original_augmented(self) -> FloatArray:
        return self._original.copy()

    def solution(self) -> FloatArray:
        return np.linalg.solve(self._echelon[:, :-1], self._echelon[:, -1])

    def steps(self) -> tuple[BackSubstitutionStep, ...]:
        x, y, z = self.solution()
        return (
            BackSubstitutionStep(
                variable="z",
                equation_tex=r"-7z=-7",
                solved_tex=r"z=1",
                value=float(z),
            ),
            BackSubstitutionStep(
                variable="y",
                equation_tex=r"y-2(1)=-1",
                solved_tex=r"y=1",
                value=float(y),
            ),
            BackSubstitutionStep(
                variable="x",
                equation_tex=r"x+1+1=3",
                solved_tex=r"x=1",
                value=float(x),
            ),
        )

    def original_equations_tex(self) -> tuple[str, str, str]:
        return (
            r"x+y+z=3",
            r"2x-y+z=2",
            r"x+2y-z=2",
        )

    def residual_in_original(self, point: Iterable[float] | FloatArray) -> FloatArray:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        return self._original[:, :-1] @ candidate - self._original[:, -1]

    def satisfies_original(self, point: Iterable[float] | FloatArray, *, atol: float = 1e-9) -> bool:
        if atol < 0 or not np.isfinite(atol):
            raise ValueError("atol must be finite and nonnegative.")
        return bool(np.all(np.abs(self.residual_in_original(point)) <= atol))

    def snapshot(self) -> BackSubstitutionSnapshot:
        return BackSubstitutionSnapshot(
            echelon_augmented=self.echelon_augmented,
            original_augmented=self.original_augmented,
            steps=self.steps(),
            solution=self.solution(),
            original_equations_tex=self.original_equations_tex(),
        )

    @staticmethod
    def _validate_augmented(matrix: FloatArray) -> None:
        if matrix.ndim != 2:
            raise ValueError("augmented matrices must be two-dimensional.")
        if not np.isfinite(matrix).all():
            raise ValueError("augmented matrices must contain finite entries.")
