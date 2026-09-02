"""Renderer-independent least-squares model built from the pseudoinverse."""

from __future__ import annotations

import numpy as np

from engine.svd_pseudoinverse import SVDPseudoinverse


class PseudoinverseLeastSquares:
    """Expose the two projections and minimum-norm choice made by ``A^+ b``."""

    def __init__(self, target=None, matrix=None, *, tolerance: float | None = None) -> None:
        self._pseudoinverse = SVDPseudoinverse(matrix, tolerance=tolerance)
        if target is None:
            target = [3.0, 1.0, 2.0]
        self._target = self._output_vector(target)

    @property
    def matrix(self) -> np.ndarray:
        return self._pseudoinverse.matrix.copy()

    @property
    def target(self) -> np.ndarray:
        return self._target.copy()

    def pseudoinverse(self) -> np.ndarray:
        return self._pseudoinverse.pseudoinverse()

    def closest_output(self) -> np.ndarray:
        return self.matrix @ self.solution()

    def residual(self) -> np.ndarray:
        return self.target - self.closest_output()

    def solution(self) -> np.ndarray:
        return self.pseudoinverse() @ self.target

    def is_consistent(self) -> bool:
        return bool(np.allclose(self.residual(), 0.0))

    def normal_equation_residual(self) -> np.ndarray:
        return self.matrix.T @ self.residual()

    def null_generator(self) -> np.ndarray:
        direction = self._pseudoinverse.null_direction().copy()
        if direction[0] < 0:
            direction *= -1
        return direction / abs(direction[0])

    def solution_family(self, parameter: float) -> np.ndarray:
        value = self._finite_scalar(parameter)
        return self.solution() + value * self.null_generator()

    def family_output(self, parameter: float) -> np.ndarray:
        return self.matrix @ self.solution_family(parameter)

    def squared_solution_norm(self, parameter: float) -> float:
        candidate = self.solution_family(parameter)
        return float(candidate @ candidate)

    def squared_residual_norm(self, candidate) -> float:
        vector = self._domain_vector(candidate)
        residual = self.target - self.matrix @ vector
        return float(residual @ residual)

    @staticmethod
    def _finite_scalar(value: float) -> float:
        candidate = np.asarray(value, dtype=float)
        if candidate.ndim != 0 or not np.isfinite(candidate):
            raise ValueError("parameter must be a finite scalar")
        return float(candidate)

    @staticmethod
    def _domain_vector(vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (2,):
            raise ValueError("candidate must have exactly two components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("candidate entries must be finite")
        return candidate

    @staticmethod
    def _output_vector(vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (3,):
            raise ValueError("target must have exactly three components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("target entries must be finite")
        return candidate
