"""Renderer-independent mathematics for CP136: deriving the 3x3 determinant formula."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class SelectionPattern:
    permutation: tuple[int, int, int]
    sign: int
    coordinates: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    product_tex: str

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


def selection_pattern(perm: tuple[int, int, int]) -> SelectionPattern:
    coords = tuple((row, col) for row, col in enumerate(perm, start=1))
    product = "".join(rf"a_{{{row}{col}}}" for row, col in coords)
    return SelectionPattern(
        permutation=perm,
        sign=permutation_sign(perm),
        coordinates=coords,  # type: ignore[arg-type]
        product_tex=product,
    )


def all_selection_patterns() -> tuple[SelectionPattern, ...]:
    return tuple(selection_pattern(perm) for perm in permutations((1, 2, 3)))


def positive_patterns() -> tuple[SelectionPattern, ...]:
    return tuple(pattern for pattern in all_selection_patterns() if pattern.sign > 0)


def negative_patterns() -> tuple[SelectionPattern, ...]:
    return tuple(pattern for pattern in all_selection_patterns() if pattern.sign < 0)


def positive_sum_tex() -> str:
    return r"a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}"


def negative_sum_tex() -> str:
    return r"-a_{11}a_{23}a_{32}-a_{12}a_{21}a_{33}-a_{13}a_{22}a_{31}"


def determinant_formula_tex() -> str:
    return rf"\det(A)={positive_sum_tex()}{negative_sum_tex()}"


def selection_rule_lines() -> tuple[str, str, str]:
    return (
        "Choose one entry from each row.",
        "Use each column exactly once.",
        "The resulting column choices form a permutation.",
    )
