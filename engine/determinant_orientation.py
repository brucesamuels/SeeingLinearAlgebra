"""Renderer-independent mathematics for CP130: determinant sign and orientation."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Sequence
import numpy as np

UNIT_SQUARE = np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]], dtype=float)

class Orientation(str, Enum):
    PRESERVED = "preserved"
    REVERSED = "reversed"
    COLLAPSED = "collapsed"

@dataclass(frozen=True)
class OrientationExample:
    name: str
    matrix: np.ndarray
    image_vertices: np.ndarray
    signed_scale: float
    area_scale: float
    orientation: Orientation


def as_matrix_2x2(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (2, 2):
        raise ValueError("matrix must have shape (2, 2)")
    if not np.isfinite(matrix).all():
        raise ValueError("matrix entries must be finite")
    return matrix


def signed_parallelogram_area(matrix: Sequence[Sequence[float]] | np.ndarray) -> float:
    m = as_matrix_2x2(matrix)
    return float(m[0,0] * m[1,1] - m[0,1] * m[1,0])


def classify_orientation(signed_scale: float, *, tolerance: float = 1e-9) -> Orientation:
    if abs(signed_scale) <= tolerance:
        return Orientation.COLLAPSED
    return Orientation.PRESERVED if signed_scale > 0 else Orientation.REVERSED


def transform_vertices(matrix: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    m = as_matrix_2x2(matrix)
    return UNIT_SQUARE @ m.T


def build_orientation_examples() -> tuple[OrientationExample, OrientationExample]:
    positive = np.array([[2.,1.],[0.,1.]], dtype=float)
    negative = np.array([[2.,1.],[0.,-1.]], dtype=float)
    examples = []
    for name, matrix in (("preserved", positive), ("reversed", negative)):
        signed = signed_parallelogram_area(matrix)
        examples.append(OrientationExample(
            name=name,
            matrix=matrix,
            image_vertices=transform_vertices(matrix),
            signed_scale=signed,
            area_scale=abs(signed),
            orientation=classify_orientation(signed),
        ))
    return tuple(examples)


def sign_statement() -> str:
    return "The sign of the determinant records orientation."
