"""Renderer-independent mathematics for Chapter 7: powers of a diagonalizable matrix."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_MATRIX = np.array(
    [[4.0, 1.0, 0.0],
     [2.0, 3.0, 0.0],
     [0.0, 0.0, 1.0]]
)

EIGENVECTORS = np.column_stack(
    [np.array([0.0, 0.0, 1.0]),
     np.array([1.0, -2.0, 0.0]),
     np.array([1.0, 1.0, 0.0])]
)


@dataclass(frozen=True)
class MatrixPowerData:
    matrix: np.ndarray
    eigenvector_matrix: np.ndarray
    inverse_eigenvector_matrix: np.ndarray
    diagonal_matrix: np.ndarray
    exponent: int
    diagonal_power: np.ndarray
    reconstructed_power: np.ndarray
    direct_power: np.ndarray


class MatrixPowersLesson:
    """Use diagonalization to compute powers through D^k."""

    def __init__(self, exponent: int = 4) -> None:
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("exponent must be a nonnegative integer")
        self.exponent = exponent

    def data(self) -> MatrixPowerData:
        p = EIGENVECTORS.copy()
        p_inv = np.linalg.inv(p)
        d = p_inv @ DEFAULT_MATRIX @ p
        d[np.abs(d) < 1e-12] = 0.0
        d_power = np.linalg.matrix_power(d, self.exponent)
        reconstructed = p @ d_power @ p_inv
        direct = np.linalg.matrix_power(DEFAULT_MATRIX, self.exponent)
        return MatrixPowerData(
            matrix=DEFAULT_MATRIX.copy(),
            eigenvector_matrix=p,
            inverse_eigenvector_matrix=p_inv,
            diagonal_matrix=d,
            exponent=self.exponent,
            diagonal_power=d_power,
            reconstructed_power=reconstructed,
            direct_power=direct,
        )

    def power_formula_holds(self) -> bool:
        data = self.data()
        return bool(np.allclose(data.reconstructed_power, data.direct_power))

    def diagonal_power_is_entrywise(self) -> bool:
        data = self.data()
        expected = np.diag(np.diag(data.diagonal_matrix) ** self.exponent)
        return bool(np.allclose(data.diagonal_power, expected))
