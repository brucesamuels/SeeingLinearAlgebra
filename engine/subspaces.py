from __future__ import annotations
from typing import Sequence
import numpy as np
from engine.vectors import Vector

class Subspace:
    def __init__(self, spanning_vectors: Sequence[Vector], tolerance=1e-10):
        if not spanning_vectors:
            raise ValueError("Use Subspace.zero(n) for the zero subspace.")
        if len({v.dimension for v in spanning_vectors}) != 1:
            raise ValueError("All vectors must share an ambient dimension.")
        self._tol = float(tolerance)
        self._ambient = spanning_vectors[0].dimension
        self._basis = self._independent(spanning_vectors)

    @classmethod
    def zero(cls, ambient_dimension: int):
        obj = cls.__new__(cls)
        obj._tol = 1e-10
        obj._ambient = ambient_dimension
        obj._basis = tuple()
        return obj

    @property
    def ambient_dimension(self): return self._ambient
    @property
    def dimension(self): return len(self._basis)
    @property
    def rank(self): return self.dimension
    @property
    def basis(self): return self._basis
    @property
    def is_zero(self): return self.dimension == 0
    @property
    def is_full_space(self): return self.dimension == self.ambient_dimension

    def _matrix(self):
        if self.is_zero:
            return np.empty((self.ambient_dimension, 0))
        return np.column_stack([v.components for v in self.basis])

    def _independent(self, vectors):
        chosen, current, rank = [], np.empty((self._ambient, 0)), 0
        for v in vectors:
            candidate = np.column_stack([current, v.components])
            new_rank = np.linalg.matrix_rank(candidate, tol=self._tol)
            if new_rank > rank:
                chosen.append(v)
                current, rank = candidate, new_rank
        return tuple(chosen)

    def contains(self, vector: Vector):
        if vector.dimension != self.ambient_dimension:
            return False
        if self.is_zero:
            return vector.is_zero
        B = self._matrix()
        return np.linalg.matrix_rank(
            np.column_stack([B, vector.components]), tol=self._tol
        ) == np.linalg.matrix_rank(B, tol=self._tol)

    def coordinates_of(self, vector: Vector):
        if not self.contains(vector):
            raise ValueError("Vector is not in the subspace.")
        if self.is_zero:
            return tuple()
        x, *_ = np.linalg.lstsq(self._matrix(), vector.components, rcond=None)
        return tuple(float(t) for t in x)

    def projection_matrix(self):
        if self.is_zero:
            return np.zeros((self.ambient_dimension, self.ambient_dimension))
        q, _ = np.linalg.qr(self._matrix())
        q = q[:, :self.dimension]
        return q @ q.T

    def project(self, vector: Vector):
        if vector.dimension != self.ambient_dimension:
            raise ValueError("Vector belongs to a different ambient space.")
        return Vector(self.projection_matrix() @ vector.components)

    def orthogonal_complement(self):
        if self.is_zero:
            return Subspace([Vector(np.eye(self.ambient_dimension)[:, i])
                             for i in range(self.ambient_dimension)])
        _, s, vh = np.linalg.svd(self._matrix().T, full_matrices=True)
        r = int(np.sum(s > self._tol))
        rows = vh[r:]
        return Subspace.zero(self.ambient_dimension) if rows.size == 0 else \
               Subspace([Vector(row) for row in rows])
