"""Renderer-independent mathematics for matrix-matrix multiplication."""

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


def matrix_columns(matrix: Iterable[Iterable[Number]]) -> tuple[tuple[Number, ...], ...]:
    normalized = _normalize_matrix(matrix)
    return tuple(
        tuple(row[column_index] for row in normalized)
        for column_index in range(len(normalized[0]))
    )


def dot_product(left: Iterable[Number], right: Iterable[Number]) -> Number:
    a = tuple(left)
    b = tuple(right)
    if len(a) != len(b):
        raise ValueError("dot product requires equal lengths")
    return sum(x * y for x, y in zip(a, b))


def matrices_are_compatible(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> bool:
    left_shape = matrix_shape(left)
    right_shape = matrix_shape(right)
    return left_shape[1] == right_shape[0]


def product_shape(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> tuple[int, int]:
    left_shape = matrix_shape(left)
    right_shape = matrix_shape(right)
    if left_shape[1] != right_shape[0]:
        raise ValueError("inner dimensions must match")
    return left_shape[0], right_shape[1]


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
        tuple(dot_product(row, column) for column in columns)
        for row in a
    )


@dataclass(frozen=True)
class EntryComputation:
    row_index: int
    column_index: int
    row: tuple[Number, ...]
    column: tuple[Number, ...]
    products: tuple[Number, ...]
    result: Number


def entry_computations(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> tuple[EntryComputation, ...]:
    a = _normalize_matrix(left)
    b = _normalize_matrix(right)
    if len(a[0]) != len(b):
        raise ValueError("inner dimensions must match")

    columns = matrix_columns(b)
    computations: list[EntryComputation] = []
    for row_index, row in enumerate(a):
        for column_index, column in enumerate(columns):
            products = tuple(x * y for x, y in zip(row, column))
            computations.append(
                EntryComputation(
                    row_index=row_index,
                    column_index=column_index,
                    row=row,
                    column=column,
                    products=products,
                    result=sum(products),
                )
            )
    return tuple(computations)


@dataclass(frozen=True)
class MatrixMatrixMultiplicationLesson:
    left: MatrixData
    right: MatrixData
    incompatible_left_shape: tuple[int, int]
    incompatible_right_shape: tuple[int, int]

    @property
    def result(self) -> MatrixData:
        return multiply_matrices(self.left, self.right)

    @property
    def result_shape(self) -> tuple[int, int]:
        return product_shape(self.left, self.right)

    @property
    def computations(self) -> tuple[EntryComputation, ...]:
        return entry_computations(self.left, self.right)


MATRIX_MATRIX_MULTIPLICATION_LESSON = MatrixMatrixMultiplicationLesson(
    left=((1, 2, -1), (3, 0, 4)),
    right=((2, 1), (-1, 3), (5, 2)),
    incompatible_left_shape=(2, 3),
    incompatible_right_shape=(2, 2),
)
