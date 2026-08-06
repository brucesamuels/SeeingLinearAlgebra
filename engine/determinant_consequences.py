"""Renderer-independent mathematics for CP133: derived determinant consequences.

This checkpoint continues the running sequence "Properties of the Determinant"
and derives several consequences from the foundational properties:

4. Equal rows imply determinant zero.
5. A zero row implies determinant zero.
6. Adding a multiple of one row to another leaves the determinant unchanged.
7. Dependent rows imply determinant zero.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

UNIT_SQUARE = np.array(
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
    dtype=float,
)


@dataclass(frozen=True)
class MatrixExample:
    matrix: np.ndarray
    determinant: float
    image_vertices: np.ndarray


@dataclass(frozen=True)
class RowReplacementExample:
    original: MatrixExample
    replaced: MatrixExample
    multiple: float


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


def row_replacement(
    values: Sequence[Sequence[float]] | np.ndarray,
    target_row: int,
    source_row: int,
    multiple: float,
) -> np.ndarray:
    matrix = as_matrix_2x2(values).copy()
    if target_row not in (0, 1) or source_row not in (0, 1):
        raise ValueError("row indices must be 0 or 1")
    if target_row == source_row:
        raise ValueError("target_row and source_row must differ")
    matrix[target_row] = matrix[target_row] + float(multiple) * matrix[source_row]
    return matrix


def build_equal_rows_example() -> MatrixExample:
    matrix = np.array([[1.0, 2.0], [1.0, 2.0]], dtype=float)
    return MatrixExample(matrix, determinant_2x2(matrix), transform_unit_square(matrix))


def build_zero_row_example() -> MatrixExample:
    matrix = np.array([[0.0, 0.0], [1.0, 2.0]], dtype=float)
    return MatrixExample(matrix, determinant_2x2(matrix), transform_unit_square(matrix))


def build_row_replacement_example() -> RowReplacementExample:
    original_matrix = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float)
    replaced_matrix = row_replacement(original_matrix, 0, 1, -2.0)
    original = MatrixExample(
        original_matrix,
        determinant_2x2(original_matrix),
        transform_unit_square(original_matrix),
    )
    replaced = MatrixExample(
        replaced_matrix,
        determinant_2x2(replaced_matrix),
        transform_unit_square(replaced_matrix),
    )
    return RowReplacementExample(original, replaced, -2.0)


def build_dependent_rows_example() -> MatrixExample:
    matrix = np.array([[2.0, 4.0], [1.0, 2.0]], dtype=float)
    return MatrixExample(matrix, determinant_2x2(matrix), transform_unit_square(matrix))


def summary_lines() -> tuple[str, str, str, str]:
    return (
        "Property 4: Equal rows imply determinant zero.",
        "Property 5: A zero row implies determinant zero.",
        "Property 6: Adding a multiple of one row to another leaves the determinant unchanged.",
        "Property 7: Dependent rows imply determinant zero.",
    )
