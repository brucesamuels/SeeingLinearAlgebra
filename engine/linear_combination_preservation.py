"""Renderer-independent mathematics for CP86.

A linear transformation preserves arbitrary linear combinations.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]
Matrix = NDArray[np.float64]


@dataclass(frozen=True)
class LinearCombinationPreservationSnapshot:
    matrix: Matrix
    u: Vector
    v: Vector
    a: float
    b: float
    au: Vector
    bv: Vector
    combination: Vector
    transformed_u: Vector
    transformed_v: Vector
    scaled_transformed_u: Vector
    scaled_transformed_v: Vector
    transformed_combination: Vector
    combination_of_transforms: Vector
    residual: Vector

    @property
    def endpoints_agree(self) -> bool:
        return bool(np.allclose(self.residual, np.zeros(2), atol=1e-9))


def apply_transformation(matrix: Matrix, vector: Vector) -> Vector:
    matrix_value = np.asarray(matrix, dtype=float)
    vector_value = np.asarray(vector, dtype=float)

    if matrix_value.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    if vector_value.shape != (2,):
        raise ValueError("vector must be two-dimensional")

    return matrix_value @ vector_value


def evaluate_linear_combination_preservation(
    *,
    matrix: Matrix | None = None,
    u: Vector | None = None,
    v: Vector | None = None,
    a: float = 1.35,
    b: float = -0.85,
) -> LinearCombinationPreservationSnapshot:
    matrix_value = (
        np.array([[1.10, 0.45], [-0.25, 0.90]], dtype=float)
        if matrix is None
        else np.asarray(matrix, dtype=float)
    )
    u_value = (
        np.array([1.35, 0.45], dtype=float)
        if u is None
        else np.asarray(u, dtype=float)
    )
    v_value = (
        np.array([-0.45, 1.35], dtype=float)
        if v is None
        else np.asarray(v, dtype=float)
    )

    if matrix_value.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    if u_value.shape != (2,) or v_value.shape != (2,):
        raise ValueError("u and v must each be two-dimensional")

    au = float(a) * u_value
    bv = float(b) * v_value
    combination = au + bv

    transformed_u = apply_transformation(matrix_value, u_value)
    transformed_v = apply_transformation(matrix_value, v_value)

    scaled_transformed_u = float(a) * transformed_u
    scaled_transformed_v = float(b) * transformed_v

    transformed_combination = apply_transformation(
        matrix_value,
        combination,
    )
    combination_of_transforms = (
        scaled_transformed_u + scaled_transformed_v
    )

    return LinearCombinationPreservationSnapshot(
        matrix=matrix_value.copy(),
        u=u_value.copy(),
        v=v_value.copy(),
        a=float(a),
        b=float(b),
        au=au,
        bv=bv,
        combination=combination,
        transformed_u=transformed_u,
        transformed_v=transformed_v,
        scaled_transformed_u=scaled_transformed_u,
        scaled_transformed_v=scaled_transformed_v,
        transformed_combination=transformed_combination,
        combination_of_transforms=combination_of_transforms,
        residual=transformed_combination - combination_of_transforms,
    )
