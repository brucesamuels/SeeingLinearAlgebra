"""Mathematics for CP131: generalized encasement and shoelace derivations."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np

@dataclass(frozen=True)
class SymbolicDerivation:
    vertices: tuple[str, str, str, str]
    rectangle_area: str
    outside_pieces: tuple[str, ...]
    outside_total: str
    encasement_result: str
    forward_products: tuple[str, ...]
    backward_products: tuple[str, ...]
    shoelace_result: str


def as_matrix_2x2(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (2, 2):
        raise ValueError("matrix must have shape (2, 2)")
    if not np.isfinite(matrix).all():
        raise ValueError("matrix entries must be finite")
    return matrix


def determinant(values: Sequence[Sequence[float]] | np.ndarray) -> float:
    a, b = as_matrix_2x2(values)[0]
    c, d = as_matrix_2x2(values)[1]
    return float(a * d - b * c)


def build_symbolic_derivation() -> SymbolicDerivation:
    return SymbolicDerivation(
        vertices=("(0,0)", "(a,c)", "(a+b,c+d)", "(b,d)"),
        rectangle_area="(a+b)(c+d)",
        outside_pieces=("ac/2", "bc", "bd/2", "bd/2", "bc", "ac/2"),
        outside_total="ac+bd+2bc",
        encasement_result="(a+b)(c+d)-(ac+bd+2bc)=ad-bc",
        forward_products=("0c", "a(c+d)", "(a+b)d", "b0"),
        backward_products=("0a", "c(a+b)", "(c+d)b", "d0"),
        shoelace_result="1/2[(ac+2ad+bd)-(ac+2bc+bd)]=ad-bc",
    )


def final_statement() -> str:
    return "The bounding rectangle and the crossed shoelaces reveal the same signed area."
