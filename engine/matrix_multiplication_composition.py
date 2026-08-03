"""Renderer-independent mathematics for matrix multiplication as composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

Number = int | float
MatrixData = tuple[tuple[Number, ...], ...]
VectorData = tuple[Number, ...]


def _normalize_matrix(matrix: Iterable[Iterable[Number]]) -> MatrixData:
    rows = tuple(tuple(value for value in row) for row in matrix)
    if not rows:
        raise ValueError("a matrix must contain at least one row")
    width = len(rows[0])
    if width == 0:
        raise ValueError("a matrix must contain at least one column")
    if any(len(row) != width for row in rows):
        raise ValueError("matrix rows must all have the same length")
    return rows


def _normalize_vector(vector: Iterable[Number]) -> VectorData:
    values = tuple(vector)
    if not values:
        raise ValueError("a vector must contain at least one entry")
    return values


def matrix_shape(matrix: Iterable[Iterable[Number]]) -> tuple[int, int]:
    normalized = _normalize_matrix(matrix)
    return len(normalized), len(normalized[0])


def matrix_vector_product(
    matrix: Iterable[Iterable[Number]],
    vector: Iterable[Number],
) -> VectorData:
    a = _normalize_matrix(matrix)
    x = _normalize_vector(vector)
    if len(a[0]) != len(x):
        raise ValueError("matrix columns must equal vector length")
    return tuple(
        sum(value * coordinate for value, coordinate in zip(row, x))
        for row in a
    )


def matrix_columns(matrix: Iterable[Iterable[Number]]) -> tuple[VectorData, ...]:
    normalized = _normalize_matrix(matrix)
    return tuple(
        tuple(row[column_index] for row in normalized)
        for column_index in range(len(normalized[0]))
    )


def multiply_matrices(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> MatrixData:
    a = _normalize_matrix(left)
    b = _normalize_matrix(right)
    if len(a[0]) != len(b):
        raise ValueError("inner dimensions must match")
    columns = matrix_columns(b)
    return tuple(
        tuple(
            sum(x * y for x, y in zip(row, column))
            for column in columns
        )
        for row in a
    )


def compose_on_vector(
    outer: Iterable[Iterable[Number]],
    inner: Iterable[Iterable[Number]],
    vector: Iterable[Number],
) -> VectorData:
    return matrix_vector_product(
        outer,
        matrix_vector_product(inner, vector),
    )


@dataclass(frozen=True)
class MatrixCompositionLesson:
    first_matrix: MatrixData
    second_matrix: MatrixData
    vector: VectorData

    @property
    def after_first(self) -> VectorData:
        return matrix_vector_product(self.first_matrix, self.vector)

    @property
    def after_second(self) -> VectorData:
        return matrix_vector_product(self.second_matrix, self.after_first)

    @property
    def product_matrix(self) -> MatrixData:
        return multiply_matrices(self.second_matrix, self.first_matrix)

    @property
    def product_result(self) -> VectorData:
        return matrix_vector_product(self.product_matrix, self.vector)


MATRIX_COMPOSITION_LESSON = MatrixCompositionLesson(
    # First: horizontal shear (x, y) -> (x + y, y)
    first_matrix=((1, 1), (0, 1)),
    # Second: reflection across the y-axis (x, y) -> (-x, y)
    second_matrix=((-1, 0), (0, 1)),
    vector=(2, 1),
)
