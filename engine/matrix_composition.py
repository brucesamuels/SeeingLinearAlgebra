"""Renderer-independent mathematics for composing two 2D linear maps."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]

@dataclass(frozen=True)
class MatrixCompositionSnapshot:
    matrix_a: FloatArray
    matrix_b: FloatArray
    product_ab: FloatArray
    product_ba: FloatArray
    vector_x: FloatArray
    after_b: FloatArray
    after_a_after_b: FloatArray
    after_ab: FloatArray
    after_b_after_a: FloatArray

class MatrixComposition:
    def __init__(self, matrix_a=None, matrix_b=None, vector_x=None) -> None:
        self.matrix_a = np.array(
            matrix_a if matrix_a is not None else [[0.0, -1.0], [1.0, 0.0]],
            dtype=float,
        )
        self.matrix_b = np.array(
            matrix_b if matrix_b is not None else [[1.0, 1.0], [0.0, 1.0]],
            dtype=float,
        )
        self.vector_x = np.array(
            vector_x if vector_x is not None else [2.0, 1.0],
            dtype=float,
        )
        if self.matrix_a.shape != (2, 2):
            raise ValueError("matrix_a must be a 2 by 2 matrix.")
        if self.matrix_b.shape != (2, 2):
            raise ValueError("matrix_b must be a 2 by 2 matrix.")
        if self.vector_x.shape != (2,):
            raise ValueError("vector_x must contain two coordinates.")

    def snapshot(self) -> MatrixCompositionSnapshot:
        product_ab = self.matrix_a @ self.matrix_b
        product_ba = self.matrix_b @ self.matrix_a
        after_b = self.matrix_b @ self.vector_x
        after_a_after_b = self.matrix_a @ after_b
        after_ab = product_ab @ self.vector_x
        after_b_after_a = product_ba @ self.vector_x
        return MatrixCompositionSnapshot(
            self.matrix_a.copy(),
            self.matrix_b.copy(),
            product_ab,
            product_ba,
            self.vector_x.copy(),
            after_b,
            after_a_after_b,
            after_ab,
            after_b_after_a,
        )
