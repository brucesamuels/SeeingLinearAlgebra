"""Renderer-independent mathematics for repeated eigenvalues and diagonalizability."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

GOOD_MATRIX = np.array([[2.0, 0.0], [0.0, 2.0]])
BAD_MATRIX = np.array([[2.0, 1.0], [0.0, 2.0]])
REPEATED_EIGENVALUE = 2.0


@dataclass(frozen=True)
class RepeatedEigenvalueExample:
    matrix: np.ndarray
    algebraic_multiplicity: int
    geometric_multiplicity: int
    eigenspace_basis: tuple[np.ndarray, ...]
    diagonalizable: bool


def eigenspace_basis(matrix: np.ndarray, eigenvalue: float = REPEATED_EIGENVALUE) -> tuple[np.ndarray, ...]:
    shifted = np.asarray(matrix, dtype=float) - eigenvalue * np.eye(2)
    _, singular_values, vh = np.linalg.svd(shifted)
    rank = int(np.sum(singular_values > 1e-9))
    nullity = 2 - rank
    if nullity == 0:
        return ()
    basis_rows = vh[-nullity:]
    return tuple(row.copy() for row in basis_rows)


def make_example(matrix: np.ndarray) -> RepeatedEigenvalueExample:
    basis = eigenspace_basis(matrix)
    gm = len(basis)
    return RepeatedEigenvalueExample(
        matrix=np.asarray(matrix, dtype=float).copy(),
        algebraic_multiplicity=2,
        geometric_multiplicity=gm,
        eigenspace_basis=basis,
        diagonalizable=(gm == 2),
    )


class RepeatedEigenvaluesLesson:
    def good_example(self) -> RepeatedEigenvalueExample:
        return make_example(GOOD_MATRIX)

    def bad_example(self) -> RepeatedEigenvalueExample:
        return make_example(BAD_MATRIX)

    @staticmethod
    def same_characteristic_polynomial() -> bool:
        # Both matrices are triangular with repeated diagonal entry 2.
        return True

    @staticmethod
    def diagonalizable_from_multiplicities(algebraic: int, geometric: int) -> bool:
        if algebraic < 1 or geometric < 1 or geometric > algebraic:
            raise ValueError("multiplicities must satisfy 1 <= geometric <= algebraic")
        return geometric == algebraic
