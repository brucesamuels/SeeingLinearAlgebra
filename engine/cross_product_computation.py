"""Renderer-independent computation for a 3D cross product expansion."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class CrossProductComputationSnapshot:
    vector_u: FloatArray
    vector_v: FloatArray
    i_minor: FloatArray
    j_minor: FloatArray
    k_minor: FloatArray
    i_determinant: float
    j_determinant: float
    k_determinant: float
    i_coefficient: float
    j_coefficient: float
    k_coefficient: float
    result: FloatArray
    dot_u_result: float
    dot_v_result: float


class CrossProductComputation:
    """Compute a 3D cross product using first-row cofactor expansion."""

    def __init__(self, vector_u=None, vector_v=None) -> None:
        self.vector_u = np.asarray(
            vector_u if vector_u is not None else [2.0, 1.0, 3.0],
            dtype=float,
        )
        self.vector_v = np.asarray(
            vector_v if vector_v is not None else [1.0, 4.0, 2.0],
            dtype=float,
        )

        if self.vector_u.shape != (3,):
            raise ValueError("vector_u must contain exactly three coordinates.")
        if self.vector_v.shape != (3,):
            raise ValueError("vector_v must contain exactly three coordinates.")

    @staticmethod
    def determinant_2x2(matrix) -> float:
        values = np.asarray(matrix, dtype=float)
        if values.shape != (2, 2):
            raise ValueError("determinant_2x2 expects a 2 by 2 matrix.")
        return float(values[0, 0] * values[1, 1] - values[0, 1] * values[1, 0])

    def snapshot(self) -> CrossProductComputationSnapshot:
        u1, u2, u3 = self.vector_u
        v1, v2, v3 = self.vector_v

        i_minor = np.array([[u2, u3], [v2, v3]], dtype=float)
        j_minor = np.array([[u1, u3], [v1, v3]], dtype=float)
        k_minor = np.array([[u1, u2], [v1, v2]], dtype=float)

        i_det = self.determinant_2x2(i_minor)
        j_det = self.determinant_2x2(j_minor)
        k_det = self.determinant_2x2(k_minor)

        i_coefficient = i_det
        j_coefficient = -j_det
        k_coefficient = k_det

        result = np.array(
            [i_coefficient, j_coefficient, k_coefficient],
            dtype=float,
        )

        return CrossProductComputationSnapshot(
            vector_u=self.vector_u.copy(),
            vector_v=self.vector_v.copy(),
            i_minor=i_minor,
            j_minor=j_minor,
            k_minor=k_minor,
            i_determinant=i_det,
            j_determinant=j_det,
            k_determinant=k_det,
            i_coefficient=i_coefficient,
            j_coefficient=j_coefficient,
            k_coefficient=k_coefficient,
            result=result,
            dot_u_result=float(np.dot(self.vector_u, result)),
            dot_v_result=float(np.dot(self.vector_v, result)),
        )
