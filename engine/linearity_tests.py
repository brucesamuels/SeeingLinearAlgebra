"""Renderer-independent tests for linearity of planar transformations."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable
import numpy as np
Vector = np.ndarray
PlanarMap = Callable[[Vector], Vector]
def _vector(value: Iterable[float]) -> Vector:
    result = np.asarray(tuple(value), dtype=float)
    if result.shape != (2,): raise ValueError("expected a two-dimensional vector")
    if not np.all(np.isfinite(result)): raise ValueError("vector entries must be finite")
    return result
def shear(vector: Iterable[float], factor: float = 0.65) -> Vector:
    x, y = _vector(vector); return np.array([x + float(factor) * y, y])
def translation(vector: Iterable[float], offset: Iterable[float]=(1.25,0.75)) -> Vector:
    return _vector(vector) + _vector(offset)
def radial_nonlinear(vector: Iterable[float]) -> Vector:
    value = _vector(vector); return np.linalg.norm(value) * value
@dataclass(frozen=True)
class LinearityTestSnapshot:
    name: str
    origin_image: Vector
    homogeneity_left: Vector
    homogeneity_right: Vector
    additivity_left: Vector
    additivity_right: Vector
    @property
    def fixes_origin(self): return bool(np.allclose(self.origin_image, np.zeros(2)))
    @property
    def preserves_homogeneity(self): return bool(np.allclose(self.homogeneity_left, self.homogeneity_right))
    @property
    def preserves_additivity(self): return bool(np.allclose(self.additivity_left, self.additivity_right))
    @property
    def is_linear_on_tests(self): return self.fixes_origin and self.preserves_homogeneity and self.preserves_additivity
def evaluate_linearity(name: str, transformation: PlanarMap, *, vector=(1.4,0.8), other=(-0.5,1.1), scalar=1.7):
    v,u,c=_vector(vector),_vector(other),float(scalar)
    if not np.isfinite(c): raise ValueError("scalar must be finite")
    return LinearityTestSnapshot(name,_vector(transformation(np.zeros(2))),_vector(transformation(c*v)),c*_vector(transformation(v)),_vector(transformation(u+v)),_vector(transformation(u))+_vector(transformation(v)))
