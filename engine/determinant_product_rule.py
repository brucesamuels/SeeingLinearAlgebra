"""Renderer-independent mathematics for CP143: determinant of a product."""
from __future__ import annotations


def theorem_tex() -> str:
    return r"\det(AB)=\det(A)\det(B)"


def elementary_cases() -> tuple[tuple[str, str, str], ...]:
    return (
        (r"R_i\leftrightarrow R_j", r"\det(E)=-1", r"\det(EB)=-\det(B)"),
        (r"R_i\to cR_i", r"\det(E)=c", r"\det(EB)=c\det(B)"),
        (r"R_i\to R_i+cR_j", r"\det(E)=1", r"\det(EB)=\det(B)"),
    )


def elementary_conclusion_tex() -> str:
    return r"\det(EB)=\det(E)\det(B)"


def factorization_tex() -> str:
    return r"A=E_mE_{m-1}\cdots E_1"


def product_factorization_tex() -> str:
    return r"AB=E_mE_{m-1}\cdots E_1B"


def invertible_chain_tex() -> tuple[str, ...]:
    return (
        r"\det(AB)=\det(E_m)\cdots\det(E_1)\det(B)",
        r"\det(A)=\det(E_m)\cdots\det(E_1)",
        r"\therefore\ \det(AB)=\det(A)\det(B)",
    )


def singular_case_tex() -> tuple[str, ...]:
    return (
        r"A\text{ singular}\ \Longrightarrow\ \det(A)=0",
        r"\operatorname{rank}(AB)\leq\operatorname{rank}(A)<n",
        r"AB\text{ singular}\ \Longrightarrow\ \det(AB)=0",
        r"\det(AB)=0=\det(A)\det(B)",
    )


def inverse_consequence_tex() -> tuple[str, ...]:
    return (
        r"AA^{-1}=I",
        r"\det(A)\det(A^{-1})=1",
        r"\det(A^{-1})=\frac{1}{\det(A)}",
    )


def power_consequence_tex() -> str:
    return r"\det(A^k)=\det(A)^k"


def many_factors_tex() -> str:
    return r"\det(A_1A_2\cdots A_m)=\det(A_1)\det(A_2)\cdots\det(A_m)"


def closing_lines() -> tuple[str, ...]:
    return (
        "Each elementary row operation contributes the same determinant factor to E and to EB.",
        "Products of elementary matrices extend that rule to every invertible matrix.",
        "If A is singular, then AB is singular, so the same formula still holds.",
    )
