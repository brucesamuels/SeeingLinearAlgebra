"""Renderer-independent mathematics for CP139: triangular determinants."""
from __future__ import annotations


def upper_triangular_example() -> tuple[tuple[int, ...], ...]:
    return (
        (2, 3, -1, 4),
        (0, -2, 5, 1),
        (0, 0, 3, 7),
        (0, 0, 0, 4),
    )


def upper_triangular_diagonal() -> tuple[int, ...]:
    return (2, -2, 3, 4)


def upper_triangular_determinant() -> int:
    product = 1
    for value in upper_triangular_diagonal():
        product *= value
    return product


def diagonal_product_tex() -> str:
    return r"\det(U)=2(-2)(3)(4)=-48"


def triangular_rule_tex() -> str:
    return r"\det(T)=t_{11}t_{22}\cdots t_{nn}"


def triangular_explanation_lines() -> tuple[str, ...]:
    return (
        "Expand along a row or column containing many zeros.",
        "At each stage, another diagonal entry is selected.",
        "The recursion continues until only 1x1 determinants remain.",
    )


def lower_triangular_example() -> tuple[tuple[int, ...], ...]:
    return (
        (5, 0, 0),
        (2, -1, 0),
        (4, 3, 6),
    )


def lower_triangular_determinant() -> int:
    return 5 * (-1) * 6


def block_triangular_symbolic_tex() -> str:
    return r"M=\begin{bmatrix}A&B\\0&D\end{bmatrix}"


def block_triangular_rule_tex() -> str:
    return r"\det(M)=\det(A)\det(D)"


def block_example_tex() -> str:
    return (
        r"M=\begin{bmatrix}"
        r"2&1&3&0\\"
        r"0&4&1&2\\"
        r"0&0&-1&5\\"
        r"0&0&0&3"
        r"\end{bmatrix}"
    )


def block_example_factorization_tex() -> str:
    return (
        r"\det(M)="
        r"\det\begin{bmatrix}2&1\\0&4\end{bmatrix}"
        r"\det\begin{bmatrix}-1&5\\0&3\end{bmatrix}"
        r"=(8)(-3)=-24"
    )


def strategy_lines() -> tuple[str, ...]:
    return (
        "Before expanding or eliminating, look for structure.",
        "Triangular matrices: multiply the diagonal entries.",
        "Block-triangular matrices: multiply the block determinants.",
    )
