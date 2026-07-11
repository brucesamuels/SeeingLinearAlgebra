from __future__ import annotations
from dataclasses import dataclass
from numbers import Real
from typing import Iterable, Sequence
import numpy as np

def _array(values: Iterable[Real]) -> np.ndarray:
    a = np.asarray(list(values), dtype=float)
    if a.ndim != 1 or a.size == 0:
        raise ValueError("Vector components must be a nonempty one-dimensional sequence.")
    return a

@dataclass(frozen=True)
class Vector:
    components: np.ndarray

    def __init__(self, components: Iterable[Real]):
        object.__setattr__(self, "components", _array(components))

    @property
    def dimension(self) -> int:
        return int(self.components.size)

    @property
    def magnitude(self) -> float:
        return float(np.linalg.norm(self.components))

    @property
    def is_zero(self) -> bool:
        return bool(np.allclose(self.components, 0.0))

    def normalized(self) -> "Vector":
        if self.is_zero:
            raise ValueError("The zero vector cannot be normalized.")
        return Vector(self.components / self.magnitude)

    def scale(self, scalar: Real) -> "Vector":
        return Vector(float(scalar) * self.components)

    def _check(self, other: "Vector"):
        if self.dimension != other.dimension:
            raise ValueError("Vectors must lie in the same ambient space.")

    def dot(self, other: "Vector") -> float:
        self._check(other)
        return float(np.dot(self.components, other.components))

    def coordinates(self) -> tuple[float, ...]:
        return tuple(float(x) for x in self.components)

    def standard_basis_expansion(self):
        return [(float(x), BasisVector(i + 1, self.dimension))
                for i, x in enumerate(self.components)]

    def __add__(self, other):
        self._check(other)
        return Vector(self.components + other.components)

    def __sub__(self, other):
        self._check(other)
        return Vector(self.components - other.components)

    def __mul__(self, scalar):
        return self.scale(scalar) if isinstance(scalar, Real) else NotImplemented

    __rmul__ = __mul__

    def __neg__(self):
        return self.scale(-1)

class BasisVector(Vector):
    def __init__(self, index: int, dimension: int):
        if dimension < 1 or not 1 <= index <= dimension:
            raise ValueError("Require dimension >= 1 and 1 <= index <= dimension.")
        values = np.zeros(dimension)
        values[index - 1] = 1
        super().__init__(values)
        self.index = index

    @classmethod
    def x(cls, dimension=2): return cls(1, dimension)
    @classmethod
    def y(cls, dimension=2): return cls(2, dimension)
    @classmethod
    def z(cls, dimension=3): return cls(3, dimension)

def standard_basis(dimension: int):
    return tuple(BasisVector(i, dimension) for i in range(1, dimension + 1))

class LinearCombination:
    def __init__(self, terms: Sequence[tuple[Real, Vector]]):
        if not terms:
            raise ValueError("At least one term is required.")
        dims = {v.dimension for _, v in terms}
        if len(dims) != 1:
            raise ValueError("All vectors must have the same dimension.")
        self.terms = [(float(c), v) for c, v in terms]
        self.dimension = next(iter(dims))

    @property
    def value(self):
        total = np.zeros(self.dimension)
        for c, v in self.terms:
            total += c * v.components
        return Vector(total)
