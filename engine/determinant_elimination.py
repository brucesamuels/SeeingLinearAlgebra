"""Renderer-independent mathematics for CP134: determinants and elimination.

This checkpoint uses determinant properties during elimination:
- row swaps reverse sign,
- row scaling multiplies the determinant,
- row replacement leaves the determinant unchanged,
- triangular determinants come from the product of the diagonal entries.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class EliminationStep:
    matrix: np.ndarray
    operation_text: str
    determinant_relation: str
    factor_from_start: Fraction


@dataclass(frozen=True)
class EliminationExample:
    initial_matrix: np.ndarray
    steps: tuple[EliminationStep, ...]
    triangular_matrix: np.ndarray
    triangular_diagonal: tuple[Fraction, Fraction, Fraction]
    triangular_determinant: Fraction
    original_determinant: Fraction


EXAMPLE_MATRIX = np.array(
    [[0.0, 2.0, 1.0], [1.0, 1.0, 0.0], [2.0, 3.0, 4.0]],
    dtype=float,
)


def as_matrix_3x3(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (3, 3):
        raise ValueError("matrix must have shape (3, 3)")
    if not np.isfinite(matrix).all():
        raise ValueError("matrix entries must be finite")
    return matrix


def determinant_3x3(values: Sequence[Sequence[float]] | np.ndarray) -> float:
    matrix = as_matrix_3x3(values)
    return float(np.linalg.det(matrix))


def triangular_diagonal_product(values: Sequence[Sequence[float]] | np.ndarray) -> float:
    matrix = as_matrix_3x3(values)
    return float(matrix[0, 0] * matrix[1, 1] * matrix[2, 2])


def build_elimination_example() -> EliminationExample:
    start = EXAMPLE_MATRIX.copy()
    step1 = np.array([[1.0, 1.0, 0.0], [0.0, 2.0, 1.0], [2.0, 3.0, 4.0]], dtype=float)
    step2 = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 0.5], [2.0, 3.0, 4.0]], dtype=float)
    step3 = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 0.5], [0.0, 1.0, 4.0]], dtype=float)
    step4 = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 0.5], [0.0, 0.0, 3.5]], dtype=float)

    steps = (
        EliminationStep(
            matrix=step1,
            operation_text=r"r_1 \leftrightarrow r_2",
            determinant_relation=r"\det(S_1) = -\det(A)",
            factor_from_start=Fraction(-1, 1),
        ),
        EliminationStep(
            matrix=step2,
            operation_text=r"r_2 \to \tfrac12 r_2",
            determinant_relation=r"\det(S_2) = \tfrac12\det(S_1) = -\tfrac12\det(A)",
            factor_from_start=Fraction(-1, 2),
        ),
        EliminationStep(
            matrix=step3,
            operation_text=r"r_3 \to r_3 - 2r_1",
            determinant_relation=r"\det(S_3) = \det(S_2)",
            factor_from_start=Fraction(-1, 2),
        ),
        EliminationStep(
            matrix=step4,
            operation_text=r"r_3 \to r_3 - r_2",
            determinant_relation=r"\det(U) = \det(S_3)",
            factor_from_start=Fraction(-1, 2),
        ),
    )
    triangular_diagonal = (Fraction(1, 1), Fraction(1, 1), Fraction(7, 2))
    triangular_determinant = Fraction(7, 2)
    original_determinant = Fraction(-7, 1)
    return EliminationExample(
        initial_matrix=start,
        steps=steps,
        triangular_matrix=step4,
        triangular_diagonal=triangular_diagonal,
        triangular_determinant=triangular_determinant,
        original_determinant=original_determinant,
    )


def overview_rule_lines() -> tuple[str, str, str, str]:
    return (
        "Swap rows -> change the sign.",
        "Scale a row -> multiply the determinant by that scale factor.",
        "Add a multiple of one row to another -> determinant unchanged.",
        "For the resulting triangular matrix U, det(U) is the product of the diagonal.",
    )
