"""Renderer-independent mathematics for CP142: adjugate and inverse formula."""
from __future__ import annotations


def cofactor_signs() -> tuple[tuple[str, ...], ...]:
    return (("+", "-", "+"), ("-", "+", "-"), ("+", "-", "+"))


def adjugate_definition_tex() -> str:
    return r"\operatorname{adj}(A)=C^T\quad\text{where }C=[C_{ij}]\text{ is the cofactor matrix}"


def identity_tex() -> str:
    return r"A\operatorname{adj}(A)=\det(A)I"


def inverse_formula_tex() -> str:
    return r"A^{-1}=\frac{1}{\det(A)}\operatorname{adj}(A)\quad\text{when }\det(A)\neq0"


def diagonal_entry_tex() -> str:
    return r"\text{Diagonal entries are cofactor expansions of }\det(A)"


def off_diagonal_entry_tex() -> str:
    return r"\text{Off-diagonal entries are }0\text{ because the expansion has two equal rows}"


def example_matrix() -> tuple[tuple[int, ...], ...]:
    return ((2, 1), (5, 3))


def example_determinant() -> int:
    return 1


def example_cofactor_matrix() -> tuple[tuple[int, ...], ...]:
    return ((3, -5), (-1, 2))


def example_adjugate() -> tuple[tuple[int, ...], ...]:
    return ((3, -1), (-5, 2))


def example_inverse_formula_tex() -> str:
    return (
        r"\begin{bmatrix}2&1\\5&3\end{bmatrix}^{-1}"
        r"=\frac{1}{2\cdot3-1\cdot5}"
        r"\begin{bmatrix}3&-1\\-5&2\end{bmatrix}"
        r"=\begin{bmatrix}3&-1\\-5&2\end{bmatrix}"
    )


def example_product_tex() -> str:
    return (
        r"\begin{bmatrix}2&1\\5&3\end{bmatrix}"
        r"\begin{bmatrix}3&-1\\-5&2\end{bmatrix}"
        r"=\begin{bmatrix}1&0\\0&1\end{bmatrix}"
    )


def cramer_connection_tex() -> tuple[str, ...]:
    return (
        r"\mathbf x=A^{-1}\mathbf b",
        r"\mathbf x=\frac{1}{\det(A)}\operatorname{adj}(A)\mathbf b",
        r"\text{Cramer's Rule is the column-by-column form of this formula}",
    )


def closing_lines() -> tuple[str, ...]:
    return (
        "Cofactors assemble into the adjugate.",
        "The adjugate satisfies A adj(A) = det(A) I.",
        "When det(A) is nonzero, dividing gives the inverse formula.",
    )
