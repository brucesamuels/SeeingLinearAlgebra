"""Renderer-independent mathematics for order, identity, and undoing."""

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


def identity_matrix(size: int) -> MatrixData:
    if size <= 0:
        raise ValueError("size must be positive")
    return tuple(
        tuple(
            1 if row_index == column_index else 0
            for column_index in range(size)
        )
        for row_index in range(size)
    )


@dataclass(frozen=True)
class MatrixOrderIdentityUndoingLesson:
    shear: MatrixData
    reflection: MatrixData
    vector: VectorData
    projection: MatrixData

    @property
    def shear_then_reflection_matrix(self) -> MatrixData:
        return multiply_matrices(self.reflection, self.shear)

    @property
    def reflection_then_shear_matrix(self) -> MatrixData:
        return multiply_matrices(self.shear, self.reflection)

    @property
    def shear_then_reflection_vector(self) -> VectorData:
        return matrix_vector_product(
            self.shear_then_reflection_matrix,
            self.vector,
        )

    @property
    def reflection_then_shear_vector(self) -> VectorData:
        return matrix_vector_product(
            self.reflection_then_shear_matrix,
            self.vector,
        )

    @property
    def identity(self) -> MatrixData:
        return identity_matrix(len(self.vector))

    @property
    def identity_result(self) -> VectorData:
        return matrix_vector_product(self.identity, self.vector)

    @property
    def projected_vector(self) -> VectorData:
        return matrix_vector_product(self.projection, self.vector)

    @property
    def shear_inverse(self) -> MatrixData:
        return ((1, -1), (0, 1))

    @property
    def inverse_then_shear(self) -> MatrixData:
        return multiply_matrices(self.shear_inverse, self.shear)

    @property
    def shear_then_inverse(self) -> MatrixData:
        return multiply_matrices(self.shear, self.shear_inverse)


MATRIX_ORDER_IDENTITY_UNDOING_LESSON = MatrixOrderIdentityUndoingLesson(
    shear=((1, 1), (0, 1)),
    reflection=((-1, 0), (0, 1)),
    vector=(2, 1),
    projection=((1, 0), (0, 0)),
)
