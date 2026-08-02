from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class BasisImagesToMatrixSnapshot:
    matrix: np.ndarray
    e1: np.ndarray
    e2: np.ndarray
    te1: np.ndarray
    te2: np.ndarray
    assembled: np.ndarray

    @property
    def columns_match(self) -> bool:
        return bool(np.allclose(self.matrix, self.assembled, atol=1e-9))

def evaluate_basis_images_to_matrix(matrix=None):
    A = np.array([[1.15, 0.55], [-0.20, 1.05]] if matrix is None else matrix, dtype=float)
    if A.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    e1 = np.array([1.0, 0.0])
    e2 = np.array([0.0, 1.0])
    te1 = A @ e1
    te2 = A @ e2
    assembled = np.column_stack([te1, te2])
    return BasisImagesToMatrixSnapshot(A, e1, e2, te1, te2, assembled)
