"""Renderer-independent mathematics for CP132: foundational determinant properties.

This checkpoint presents the determinant as a function characterized by three
foundational properties in 2D:

1. det(I) = 1.
2. Swapping two rows changes the sign.
3. Linearity in one row separately, shown through scaling and additivity.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

UNIT_SQUARE = np.array(
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=float
)


@dataclass(frozen=True)
class MatrixExample:
    matrix: np.ndarray
    determinant: float
    image_vertices: np.ndarray


@dataclass(frozen=True)
class AdditivityExample:
    row_piece_one: np.ndarray
    row_piece_two: np.ndarray
    fixed_row: np.ndarray
    combined_row: np.ndarray
    determinant_piece_one: float
    determinant_piece_two: float
    determinant_total: float


def as_matrix_2x2(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (2, 2):
        raise ValueError("matrix must have shape (2, 2)")
    if not np.isfinite(matrix).all():
        raise ValueError("matrix entries must be finite")
    return matrix


def determinant_2x2(values: Sequence[Sequence[float]] | np.ndarray) -> float:
    matrix = as_matrix_2x2(values)
    a, b = matrix[0]
    c, d = matrix[1]
    return float(a * d - b * c)


def transform_unit_square(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = as_matrix_2x2(values)
    return UNIT_SQUARE @ matrix.T


def row_swap(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = as_matrix_2x2(values).copy()
    matrix[[0, 1]] = matrix[[1, 0]]
    return matrix


def scale_row(
    values: Sequence[Sequence[float]] | np.ndarray,
    row_index: int,
    scale_factor: float,
) -> np.ndarray:
    matrix = as_matrix_2x2(values).copy()
    if row_index not in (0, 1):
        raise ValueError("row_index must be 0 or 1")
    matrix[row_index] *= float(scale_factor)
    return matrix


def build_identity_example() -> MatrixExample:
    matrix = np.eye(2, dtype=float)
    return MatrixExample(
        matrix=matrix,
        determinant=determinant_2x2(matrix),
        image_vertices=transform_unit_square(matrix),
    )


def build_row_swap_examples() -> tuple[MatrixExample, MatrixExample]:
    base = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float)
    swapped = row_swap(base)
    return (
        MatrixExample(base, determinant_2x2(base), transform_unit_square(base)),
        MatrixExample(swapped, determinant_2x2(swapped), transform_unit_square(swapped)),
    )


def build_row_scaling_examples() -> tuple[MatrixExample, MatrixExample, float]:
    base = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float)
    factor = 2.0
    scaled = scale_row(base, 0, factor)
    return (
        MatrixExample(base, determinant_2x2(base), transform_unit_square(base)),
        MatrixExample(scaled, determinant_2x2(scaled), transform_unit_square(scaled)),
        factor,
    )


def build_additivity_example() -> AdditivityExample:
    row_piece_one = np.array([1.0, 0.0], dtype=float)
    row_piece_two = np.array([1.0, 1.0], dtype=float)
    fixed_row = np.array([1.0, 2.0], dtype=float)
    combined_row = row_piece_one + row_piece_two
    determinant_piece_one = determinant_2x2([row_piece_one, fixed_row])
    determinant_piece_two = determinant_2x2([row_piece_two, fixed_row])
    determinant_total = determinant_2x2([combined_row, fixed_row])
    return AdditivityExample(
        row_piece_one=row_piece_one,
        row_piece_two=row_piece_two,
        fixed_row=fixed_row,
        combined_row=combined_row,
        determinant_piece_one=determinant_piece_one,
        determinant_piece_two=determinant_piece_two,
        determinant_total=determinant_total,
    )


def property_summary_lines() -> tuple[str, str, str, str]:
    return (
        "Property 1: det(I) = 1.",
        "Property 2: Swapping two rows changes the sign.",
        "Property 3a: Scaling one row scales the determinant.",
        "Property 3b: The determinant is additive in one row.",
    )
