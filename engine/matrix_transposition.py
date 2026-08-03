"""Renderer-independent mathematics for matrix transposition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

Number = int | float
MatrixData = tuple[tuple[Number, ...], ...]


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


def matrix_shape(matrix: Iterable[Iterable[Number]]) -> tuple[int, int]:
    normalized = _normalize_matrix(matrix)
    return len(normalized), len(normalized[0])


def transpose(matrix: Iterable[Iterable[Number]]) -> MatrixData:
    normalized = _normalize_matrix(matrix)
    return tuple(
        tuple(row[column_index] for row in normalized)
        for column_index in range(len(normalized[0]))
    )


def add_matrices(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> MatrixData:
    a = _normalize_matrix(left)
    b = _normalize_matrix(right)
    if matrix_shape(a) != matrix_shape(b):
        raise ValueError("matrix addition requires equal dimensions")
    return tuple(
        tuple(x + y for x, y in zip(a_row, b_row))
        for a_row, b_row in zip(a, b)
    )


def scale_matrix(
    scalar: Number,
    matrix: Iterable[Iterable[Number]],
) -> MatrixData:
    normalized = _normalize_matrix(matrix)
    return tuple(
        tuple(scalar * value for value in row)
        for row in normalized
    )


def matrix_columns(matrix: Iterable[Iterable[Number]]) -> tuple[tuple[Number, ...], ...]:
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


def is_symmetric(matrix: Iterable[Iterable[Number]]) -> bool:
    normalized = _normalize_matrix(matrix)
    return matrix_shape(normalized)[0] == matrix_shape(normalized)[1] and transpose(normalized) == normalized


@dataclass(frozen=True)
class MatrixTranspositionLesson:
    matrix: MatrixData
    second_matrix: MatrixData
    scalar: Number
    left_factor: MatrixData
    right_factor: MatrixData
    symmetric_matrix: MatrixData

    @property
    def transposed(self) -> MatrixData:
        return transpose(self.matrix)

    @property
    def double_transpose(self) -> MatrixData:
        return transpose(self.transposed)

    @property
    def transpose_sum(self) -> MatrixData:
        return transpose(add_matrices(self.matrix, self.second_matrix))

    @property
    def sum_transposes(self) -> MatrixData:
        return add_matrices(transpose(self.matrix), transpose(self.second_matrix))

    @property
    def transpose_scaled(self) -> MatrixData:
        return transpose(scale_matrix(self.scalar, self.matrix))

    @property
    def scaled_transpose(self) -> MatrixData:
        return scale_matrix(self.scalar, transpose(self.matrix))

    @property
    def transpose_product(self) -> MatrixData:
        return transpose(multiply_matrices(self.left_factor, self.right_factor))

    @property
    def reversed_transpose_product(self) -> MatrixData:
        return multiply_matrices(
            transpose(self.right_factor),
            transpose(self.left_factor),
        )


MATRIX_TRANSPOSITION_LESSON = MatrixTranspositionLesson(
    matrix=((1, 2, -1), (3, 0, 4)),
    second_matrix=((2, -1, 5), (0, 3, 1)),
    scalar=-2,
    left_factor=((1, 2), (0, -1)),
    right_factor=((3, 1), (4, 2)),
    symmetric_matrix=((2, -1, 3), (-1, 4, 0), (3, 0, 5)),
)
