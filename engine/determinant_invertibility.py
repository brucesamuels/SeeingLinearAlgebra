"""Renderer-independent mathematics for CP140: determinant and invertibility."""
from __future__ import annotations


def invertible_example() -> tuple[tuple[int, ...], ...]:
    return ((2, 1, 0), (0, 3, 1), (0, 0, 4))


def invertible_determinant() -> int:
    return 24


def singular_example() -> tuple[tuple[int, ...], ...]:
    return ((1, 2, 3), (2, 4, 6), (0, 1, 1))


def singular_determinant() -> int:
    return 0


def singular_null_vector() -> tuple[int, ...]:
    return (-1, -1, 1)


def invertible_chain_tex() -> tuple[str, ...]:
    return (
        r"\det(A)\neq 0",
        r"\Longleftrightarrow\ \text{a pivot in every row and column}",
        r"\Longleftrightarrow\ \operatorname{rank}(A)=n",
        r"\Longleftrightarrow\ \mathcal N(A)=\{\mathbf 0\}",
        r"\Longleftrightarrow\ A\text{ is invertible}",
    )


def singular_chain_tex() -> tuple[str, ...]:
    return (
        r"\det(A)=0",
        r"\Longleftrightarrow\ \text{at least one pivot is missing}",
        r"\Longleftrightarrow\ \operatorname{rank}(A)<n",
        r"\Longleftrightarrow\ \mathcal N(A)\neq\{\mathbf 0\}",
        r"\Longleftrightarrow\ A\text{ is singular}",
    )



def nullspace_invertibility_theorem_tex() -> str:
    return r"A\text{ is invertible}\quad\Longleftrightarrow\quad\mathcal N(A)=\{\mathbf 0\}"


def homogeneous_system_statement_tex() -> str:
    return r"A\mathbf x=\mathbf 0\text{ has only the trivial solution }\mathbf x=\mathbf 0"

def null_vector_equation_tex() -> str:
    return (
        r"\begin{bmatrix}1&2&3\\2&4&6\\0&1&1\end{bmatrix}"
        r"\begin{bmatrix}-1\\-1\\1\end{bmatrix}"
        r"=\begin{bmatrix}0\\0\\0\end{bmatrix}"
    )


def geometric_lines() -> tuple[str, ...]:
    return (
        "A nonzero determinant means no dimension is lost.",
        "The transformation scales signed volume by det(A).",
        "A zero determinant means the transformation collapses dimension.",
    )


def closing_lines() -> tuple[str, ...]:
    return (
        "For a square matrix, the determinant is an invertibility test.",
        "det(A) != 0  ->  invertible",
        "det(A) = 0   ->  singular",
    )
