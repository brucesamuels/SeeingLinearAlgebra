"""Renderer-independent mathematics for the matrix trace.

Checkpoint 101 introduces trace as a scalar-valued function on square matrices.
Its deeper connection to eigenvalues is intentionally deferred.
"""

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


def is_square(matrix: Iterable[Iterable[Number]]) -> bool:
    rows, columns = matrix_shape(matrix)
    return rows == columns


def trace(matrix: Iterable[Iterable[Number]]) -> Number:
    normalized = _normalize_matrix(matrix)
    rows, columns = matrix_shape(normalized)
    if rows != columns:
        raise ValueError("trace is defined only for square matrices")
    return sum(normalized[index][index] for index in range(rows))


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


@dataclass(frozen=True)
class MatrixTraceLesson:
    matrix: MatrixData
    second_matrix: MatrixData
    scalar: Number
    rectangular_matrix: MatrixData
    left_factor: MatrixData
    right_factor: MatrixData

    @property
    def matrix_trace(self) -> Number:
        return trace(self.matrix)

    @property
    def sum_trace(self) -> Number:
        return trace(add_matrices(self.matrix, self.second_matrix))

    @property
    def trace_sum(self) -> Number:
        return trace(self.matrix) + trace(self.second_matrix)

    @property
    def scaled_trace(self) -> Number:
        return trace(scale_matrix(self.scalar, self.matrix))

    @property
    def scalar_trace(self) -> Number:
        return self.scalar * trace(self.matrix)

    @property
    def ab(self) -> MatrixData:
        return multiply_matrices(self.left_factor, self.right_factor)

    @property
    def ba(self) -> MatrixData:
        return multiply_matrices(self.right_factor, self.left_factor)

    @property
    def trace_ab(self) -> Number:
        return trace(self.ab)

    @property
    def trace_ba(self) -> Number:
        return trace(self.ba)


MATRIX_TRACE_LESSON = MatrixTraceLesson(
    matrix=((3, -1, 2), (4, 5, 0), (-2, 1, 6)),
    second_matrix=((1, 2, 0), (-3, 4, 1), (5, 0, -2)),
    scalar=-2,
    rectangular_matrix=((1, 2, 3), (4, 5, 6)),
    left_factor=((1, 2), (0, -1)),
    right_factor=((3, 1), (4, 2)),
)
