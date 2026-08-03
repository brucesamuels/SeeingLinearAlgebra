"""Renderer-independent mathematics for the matrix row-column rule.

Checkpoint 98 connects matrix-vector multiplication as a column combination
(CP94) with the equivalent row-dot-vector computation.
"""

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


def dot_product(left: Iterable[Number], right: Iterable[Number]) -> Number:
    a = _normalize_vector(left)
    b = _normalize_vector(right)
    if len(a) != len(b):
        raise ValueError("dot product requires equal lengths")
    return sum(x * y for x, y in zip(a, b))


def matrix_vector_product(
    matrix: Iterable[Iterable[Number]],
    vector: Iterable[Number],
) -> VectorData:
    normalized_matrix = _normalize_matrix(matrix)
    normalized_vector = _normalize_vector(vector)
    if len(normalized_matrix[0]) != len(normalized_vector):
        raise ValueError(
            "matrix-vector multiplication requires the number of matrix "
            "columns to equal the vector length"
        )
    return tuple(
        dot_product(row, normalized_vector)
        for row in normalized_matrix
    )


def matrix_columns(matrix: Iterable[Iterable[Number]]) -> tuple[VectorData, ...]:
    normalized = _normalize_matrix(matrix)
    column_count = len(normalized[0])
    return tuple(
        tuple(row[column_index] for row in normalized)
        for column_index in range(column_count)
    )


def column_combination_product(
    matrix: Iterable[Iterable[Number]],
    vector: Iterable[Number],
) -> VectorData:
    normalized_matrix = _normalize_matrix(matrix)
    normalized_vector = _normalize_vector(vector)
    columns = matrix_columns(normalized_matrix)
    if len(columns) != len(normalized_vector):
        raise ValueError(
            "column combination requires one coefficient per matrix column"
        )

    row_count = len(normalized_matrix)
    result = [0 for _ in range(row_count)]
    for coefficient, column in zip(normalized_vector, columns):
        for row_index, value in enumerate(column):
            result[row_index] += coefficient * value
    return tuple(result)


@dataclass(frozen=True)
class RowComputation:
    row_index: int
    row: VectorData
    vector: VectorData
    products: tuple[Number, ...]
    result: Number

    @property
    def expression(self) -> str:
        product_text = "+".join(
            f"({row_value})({vector_value})"
            for row_value, vector_value in zip(self.row, self.vector)
        )
        return f"{product_text}={self.result}"


def row_computations(
    matrix: Iterable[Iterable[Number]],
    vector: Iterable[Number],
) -> tuple[RowComputation, ...]:
    normalized_matrix = _normalize_matrix(matrix)
    normalized_vector = _normalize_vector(vector)
    if len(normalized_matrix[0]) != len(normalized_vector):
        raise ValueError(
            "row computations require the row length to equal vector length"
        )

    computations: list[RowComputation] = []
    for row_index, row in enumerate(normalized_matrix):
        products = tuple(
            row_value * vector_value
            for row_value, vector_value in zip(row, normalized_vector)
        )
        computations.append(
            RowComputation(
                row_index=row_index,
                row=row,
                vector=normalized_vector,
                products=products,
                result=sum(products),
            )
        )
    return tuple(computations)


@dataclass(frozen=True)
class RowColumnRuleLesson:
    matrix: MatrixData
    vector: VectorData

    @property
    def result(self) -> VectorData:
        return matrix_vector_product(self.matrix, self.vector)

    @property
    def column_combination_result(self) -> VectorData:
        return column_combination_product(self.matrix, self.vector)

    @property
    def computations(self) -> tuple[RowComputation, ...]:
        return row_computations(self.matrix, self.vector)


ROW_COLUMN_RULE_LESSON = RowColumnRuleLesson(
    matrix=((2, -1, 3), (1, 4, -2)),
    vector=(3, 2, -1),
)
