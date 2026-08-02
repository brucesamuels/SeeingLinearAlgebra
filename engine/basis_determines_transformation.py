from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]
Matrix = NDArray[np.float64]

@dataclass(frozen=True)
class BasisDeterminationSnapshot:
    matrix: Matrix
    coefficients: Vector
    e1: Vector
    e2: Vector
    x: Vector
    te1: Vector
    te2: Vector
    tx: Vector
    rebuilt_tx: Vector

    @property
    def agrees(self) -> bool:
        return bool(np.allclose(self.tx, self.rebuilt_tx, atol=1e-9))

def evaluate_basis_determination(matrix=None, coefficients=None):
    A = np.array(
        [[1.15, 0.55], [-0.20, 1.05]] if matrix is None else matrix,
        dtype=float,
    )
    c = np.array([2.0, 1.0] if coefficients is None else coefficients, dtype=float)
    if A.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    if c.shape != (2,):
        raise ValueError("coefficients must contain two entries")

    e1 = np.array([1.0, 0.0])
    e2 = np.array([0.0, 1.0])
    x = c[0] * e1 + c[1] * e2
    te1 = A @ e1
    te2 = A @ e2
    tx = A @ x
    rebuilt = c[0] * te1 + c[1] * te2
    return BasisDeterminationSnapshot(A, c, e1, e2, x, te1, te2, tx, rebuilt)
