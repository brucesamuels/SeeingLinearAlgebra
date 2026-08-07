"""Renderer-independent mathematics for CP135: the Big Formula for determinants."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Iterable


@dataclass(frozen=True)
class PermutationTerm:
    permutation: tuple[int, int, int]
    sign: int
    product_tex: str

    @property
    def sign_tex(self) -> str:
        return "+" if self.sign > 0 else "-"

    @property
    def permutation_tex(self) -> str:
        return rf"\sigma=({self.permutation[0]}\,{self.permutation[1]}\,{self.permutation[2]})"


def permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return 1 if inversions % 2 == 0 else -1


def product_tex_for_permutation(perm: tuple[int, int, int]) -> str:
    pieces = [rf"a_{{1{perm[0]}}}", rf"a_{{2{perm[1]}}}", rf"a_{{3{perm[2]}}}"]
    return " ".join(pieces)


def permutation_terms_3x3() -> tuple[PermutationTerm, ...]:
    terms: list[PermutationTerm] = []
    for perm in permutations((1, 2, 3)):
        terms.append(
            PermutationTerm(
                permutation=perm,
                sign=permutation_sign(perm),
                product_tex=product_tex_for_permutation(perm),
            )
        )
    return tuple(terms)


def positive_terms_3x3() -> tuple[PermutationTerm, ...]:
    return tuple(term for term in permutation_terms_3x3() if term.sign > 0)


def negative_terms_3x3() -> tuple[PermutationTerm, ...]:
    return tuple(term for term in permutation_terms_3x3() if term.sign < 0)


def big_formula_tex() -> str:
    return r"\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\,a_{1\sigma(1)}a_{2\sigma(2)}\cdots a_{n\sigma(n)}"


def big_formula_explanation_lines() -> tuple[str, str, str, str]:
    return (
        "Pick exactly one entry from each row.",
        "Pick exactly one entry from each column.",
        "Each valid choice comes from a permutation of the columns.",
        "The sign is positive for even permutations\nand negative for odd permutations.",
    )


def familiar_formula_3x3_tex() -> str:
    return (
        r"\det(A)=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}"
        r"-a_{11}a_{23}a_{32}-a_{12}a_{21}a_{33}-a_{13}a_{22}a_{31}"
    )


def grouped_formula_3x3_lines() -> tuple[str, str]:
    return (
        r"\text{positive: }a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}",
        r"\text{negative: }a_{11}a_{23}a_{32}+a_{12}a_{21}a_{33}+a_{13}a_{22}a_{31}",
    )


def n_factorial_terms_statement(n: int) -> str:
    return f"There are {n}! permutation products in the determinant of an {n}x{n} matrix."
