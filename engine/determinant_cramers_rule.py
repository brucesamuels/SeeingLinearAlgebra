"""Renderer-independent mathematics for CP141: Cramer's Rule."""
from __future__ import annotations


def coefficient_matrix() -> tuple[tuple[int, ...], ...]:
    return (
        (1, 2, 0),
        (0, 1, 1),
        (2, 0, 1),
    )


def right_hand_side() -> tuple[int, ...]:
    return (0, 2, 7)


def solution_vector() -> tuple[int, ...]:
    return (2, -1, 3)


def determinant_a() -> int:
    return 5


def replacement_matrices() -> tuple[tuple[tuple[int, ...], ...], ...]:
    return (
        (
            (0, 2, 0),
            (2, 1, 1),
            (7, 0, 1),
        ),
        (
            (1, 0, 0),
            (0, 2, 1),
            (2, 7, 1),
        ),
        (
            (1, 2, 0),
            (0, 1, 2),
            (2, 0, 7),
        ),
    )


def replacement_determinants() -> tuple[int, int, int]:
    return (10, -5, 15)


def column_equation_tex() -> str:
    return r"x_1\mathbf a_1+x_2\mathbf a_2+\cdots+x_n\mathbf a_n=\mathbf b"


def replacement_definition_tex() -> str:
    return r"A_k=[\mathbf a_1\ \cdots\ \mathbf a_{k-1}\ \mathbf b\ \mathbf a_{k+1}\ \cdots\ \mathbf a_n]"


def derivation_lines_tex() -> tuple[str, ...]:
    return (
        r"\det(A_k)=\det(\mathbf a_1,\ldots,\mathbf b,\ldots,\mathbf a_n)",
        r"=\det(\mathbf a_1,\ldots,\sum_{j=1}^{n}x_j\mathbf a_j,\ldots,\mathbf a_n)",
        r"=x_k\det(A)",
    )


def theorem_tex() -> str:
    return r"x_k=\frac{\det(A_k)}{\det(A)},\qquad k=1,\ldots,n"


def theorem_condition_tex() -> str:
    return r"\det(A)\neq0"


def example_system_tex() -> str:
    return (
        r"\begin{bmatrix}1&2&0\\0&1&1\\2&0&1\end{bmatrix}"
        r"\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}"
        r"=\begin{bmatrix}0\\2\\7\end{bmatrix}"
    )


def example_ratios_tex() -> tuple[str, str, str]:
    return (
        r"x_1=\frac{\det(A_1)}{\det(A)}=\frac{10}{5}=2",
        r"x_2=\frac{\det(A_2)}{\det(A)}=\frac{-5}{5}=-1",
        r"x_3=\frac{\det(A_3)}{\det(A)}=\frac{15}{5}=3",
    )


def closing_lines() -> tuple[str, ...]:
    return (
        "Cramer's Rule solves one variable with one determinant ratio.",
        "It applies when A is square and det(A) is nonzero.",
        "For large systems, elimination is usually more efficient.",
    )
