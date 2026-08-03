"""Renderer-independent mathematics for matrix addition and subtraction.

Checkpoint 96 begins the Matrix Operations chapter.  This module deliberately
keeps the mathematics separate from Manim so the computations can be tested
without a renderer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

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


def same_shape(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> bool:
    return matrix_shape(left) == matrix_shape(right)


def add_matrices(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> MatrixData:
    a = _normalize_matrix(left)
    b = _normalize_matrix(right)
    if matrix_shape(a) != matrix_shape(b):
        raise ValueError("matrix addition requires equal dimensions")
    return tuple(
        tuple(a_value + b_value for a_value, b_value in zip(a_row, b_row))
        for a_row, b_row in zip(a, b)
    )


def negate_matrix(matrix: Iterable[Iterable[Number]]) -> MatrixData:
    normalized = _normalize_matrix(matrix)
    return tuple(tuple(-value for value in row) for row in normalized)


def subtract_matrices(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
) -> MatrixData:
    return add_matrices(left, negate_matrix(right))


@dataclass(frozen=True)
class EntrywiseStep:
    row: int
    column: int
    left_value: Number
    operation: str
    right_value: Number
    result: Number

    @property
    def expression(self) -> str:
        symbol = "+" if self.operation == "add" else "-"
        return f"{self.left_value}{symbol}{self.right_value}={self.result}"


def entrywise_steps(
    left: Iterable[Iterable[Number]],
    right: Iterable[Iterable[Number]],
    *,
    operation: str,
) -> tuple[EntrywiseStep, ...]:
    a = _normalize_matrix(left)
    b = _normalize_matrix(right)
    if matrix_shape(a) != matrix_shape(b):
        raise ValueError("entrywise operations require equal dimensions")
    if operation not in {"add", "subtract"}:
        raise ValueError("operation must be 'add' or 'subtract'")

    steps: list[EntrywiseStep] = []
    for row_index, (a_row, b_row) in enumerate(zip(a, b)):
        for column_index, (a_value, b_value) in enumerate(zip(a_row, b_row)):
            result = (
                a_value + b_value
                if operation == "add"
                else a_value - b_value
            )
            steps.append(
                EntrywiseStep(
                    row=row_index,
                    column=column_index,
                    left_value=a_value,
                    operation=operation,
                    right_value=b_value,
                    result=result,
                )
            )
    return tuple(steps)


@dataclass(frozen=True)
class MatrixAdditionSubtractionLesson:
    addition_left: MatrixData
    addition_right: MatrixData
    subtraction_left: MatrixData
    subtraction_right: MatrixData
    incompatible_left_shape: tuple[int, int]
    incompatible_right_shape: tuple[int, int]

    @property
    def addition_result(self) -> MatrixData:
        return add_matrices(self.addition_left, self.addition_right)

    @property
    def subtraction_result(self) -> MatrixData:
        return subtract_matrices(self.subtraction_left, self.subtraction_right)

    @property
    def subtraction_as_addition_result(self) -> MatrixData:
        return add_matrices(
            self.subtraction_left,
            negate_matrix(self.subtraction_right),
        )


MATRIX_ADDITION_SUBTRACTION_LESSON = MatrixAdditionSubtractionLesson(
    addition_left=((2, -1), (3, 4)),
    addition_right=((5, 3), (-2, 1)),
    subtraction_left=((4, 1), (-3, 2)),
    subtraction_right=((1, -2), (5, 3)),
    incompatible_left_shape=(2, 3),
    incompatible_right_shape=(3, 2),
)
