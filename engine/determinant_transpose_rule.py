"""Renderer-independent mathematics for CP144: determinant of a transpose."""
from __future__ import annotations


def theorem_tex() -> str:
    return r"\det(A^T)=\det(A)"


def big_formula_tex() -> str:
    return r"\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n a_{i,\sigma(i)}"


def transpose_formula_tex() -> tuple[str, str]:
    return (
        r"\det(A^T)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n (A^T)_{i,\sigma(i)}",
        r"=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n a_{\sigma(i),i}",
    )


def product_rewrite_tex() -> tuple[str, str]:
    return (
        r"\prod_{i=1}^n a_{\sigma(i),i}=\prod_{j=1}^n a_{j,\sigma^{-1}(j)}",
        r"\text{Rename }j=\sigma(i).",
    )


def reindex_sum_tex() -> tuple[str, str, str]:
    return (
        r"\det(A^T)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{j=1}^n a_{j,\sigma^{-1}(j)}",
        r"\text{Let }\tau=\sigma^{-1}.",
        r"\det(A^T)=\sum_{\tau\in S_n}\operatorname{sgn}(\tau^{-1})\prod_{j=1}^n a_{j,\tau(j)}",
    )


def sign_invariance_tex() -> tuple[str, str]:
    return (
        r"\operatorname{sgn}(\tau^{-1})=\operatorname{sgn}(\tau)",
        "An inverse permutation has the same parity.",
    )


def conclusion_tex() -> tuple[str, str, str]:
    return (
        r"\det(A^T)=\sum_{\tau\in S_n}\operatorname{sgn}(\tau)\prod_{j=1}^n a_{j,\tau(j)}",
        r"=\det(A)",
        r"\det(A^T)=\det(A)",
    )


def closing_lines() -> tuple[str, str, str]:
    return (
        "Transposing swaps rows and columns.",
        "The permutation formula is unchanged after reindexing by the inverse permutation.",
        "So every determinant statement about rows has a matching statement about columns.",
    )
