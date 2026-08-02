from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class MatrixVectorColumnCombinationSnapshot:
    matrix: np.ndarray
    vector: np.ndarray
    first_column: np.ndarray
    second_column: np.ndarray
    first_contribution: np.ndarray
    second_contribution: np.ndarray
    product: np.ndarray
    reconstructed: np.ndarray

    @property
    def agrees(self) -> bool:
        return bool(np.allclose(self.product, self.reconstructed, atol=1e-9))

def evaluate_matrix_vector_column_combination(matrix=None, vector=None):
    A = np.array([[1.0, -1.0], [2.0, 1.0]] if matrix is None else matrix, dtype=float)
    x = np.array([2.0, 1.0] if vector is None else vector, dtype=float)
    if A.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    if x.shape != (2,):
        raise ValueError("vector must contain two entries")
    a1 = A[:, 0]
    a2 = A[:, 1]
    c1 = x[0] * a1
    c2 = x[1] * a2
    product = A @ x
    rebuilt = c1 + c2
    return MatrixVectorColumnCombinationSnapshot(
        A.copy(), x.copy(), a1.copy(), a2.copy(),
        c1.copy(), c2.copy(), product.copy(), rebuilt.copy()
    )
