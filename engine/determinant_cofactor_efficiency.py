"""Renderer-independent mathematics for CP138: efficient recursive cofactor expansion."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CofactorStep:
    matrix: tuple[tuple[int, ...], ...]
    row: int
    column: int
    entry: int
    sign: int
    minor: tuple[tuple[int, ...], ...]


def example_matrix() -> tuple[tuple[int, ...], ...]:
    return (
        (2, 0, 1, 0),
        (0, 3, 0, 0),
        (1, 0, 2, 1),
        (0, 0, 1, 2),
    )


def first_expansion_step() -> CofactorStep:
    # Expand along row 2: only a_22 = 3 is nonzero and (-1)^(2+2)=+1.
    return CofactorStep(
        matrix=example_matrix(),
        row=2,
        column=2,
        entry=3,
        sign=1,
        minor=((2, 1, 0), (1, 2, 1), (0, 1, 2)),
    )


def second_expansion_step() -> CofactorStep:
    # In the 3x3 minor, expand along row 1: the third entry is zero.
    return CofactorStep(
        matrix=first_expansion_step().minor,
        row=1,
        column=1,
        entry=2,
        sign=1,
        minor=((2, 1), (1, 2)),
    )


def second_expansion_other_minor() -> tuple[tuple[int, int], tuple[int, int]]:
    # Minor associated with entry a_12 = 1 in the 3x3 matrix.
    return ((1, 1), (0, 2))


def determinant_2x2(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    (a, b), (c, d) = matrix
    return a * d - b * c


def minor_3x3_value() -> int:
    # 2*det[[2,1],[1,2]] - 1*det[[1,1],[0,2]]
    return 2 * determinant_2x2(second_expansion_step().minor) - determinant_2x2(second_expansion_other_minor())


def determinant_value() -> int:
    return first_expansion_step().entry * minor_3x3_value()


def matrix_tex(matrix: tuple[tuple[int, ...], ...]) -> str:
    rows = ["&".join(str(value) for value in row) for row in matrix]
    return r"\begin{bmatrix}" + r"\\".join(rows) + r"\end{bmatrix}"


def first_expansion_tex() -> str:
    return rf"\det(A)=3\det\left({matrix_tex(first_expansion_step().minor)}\right)"


def recursive_expansion_tex() -> str:
    return (
        r"\det(B)="
        r"2\begin{vmatrix}2&1\\1&2\end{vmatrix}"
        r"-\begin{vmatrix}1&1\\0&2\end{vmatrix}"
    )


def arithmetic_lines() -> tuple[str, str, str]:
    return (
        r"\det(B)=2(4-1)-(2-0)=4",
        r"\det(A)=3\det(B)=3(4)",
        r"\det(A)=12",
    )


def strategy_lines() -> tuple[str, str, str]:
    return (
        "Cofactor expansion works along any row or column.",
        "Zeros make terms disappear.",
        "Choose a row or column with as many zeros as possible.",
    )


def comparison_counts() -> tuple[int, int]:
    """Return surviving terms for the good row and a poorer row of A."""
    return (1, 2)
