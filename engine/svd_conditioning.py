"""Renderer-independent model for singular values and conditioning."""

from __future__ import annotations

import numpy as np


class SVDConditioning:
    """Measure forward stretches and inverse sensitivity for a 2-by-2 map."""

    def __init__(self, matrix=None, *, tolerance: float | None = None) -> None:
        if matrix is None:
            matrix = [[4.0, 0.0], [0.0, 0.25]]
        candidate = np.asarray(matrix, dtype=float)
        if candidate.shape != (2, 2):
            raise ValueError("matrix must be two by two")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("matrix entries must be finite")
        self._matrix = candidate.copy()
        self._u, self._singular_values, self._vt = np.linalg.svd(self._matrix)
        if tolerance is None:
            scale = self._singular_values[0] if self._singular_values.size else 1.0
            tolerance = np.finfo(float).eps * 2 * max(scale, 1.0)
        if not np.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        self._tolerance = float(tolerance)

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    def singular_values(self) -> np.ndarray:
        return self._singular_values.copy()

    def inverse_singular_values(self) -> np.ndarray:
        result = np.full_like(self._singular_values, np.inf)
        positive = self._singular_values > self._tolerance
        result[positive] = 1.0 / self._singular_values[positive]
        return result

    def condition_number(self) -> float:
        smallest = self._singular_values[-1]
        if smallest <= self._tolerance:
            return float("inf")
        return float(self._singular_values[0] / smallest)

    def is_invertible(self) -> bool:
        return bool(self._singular_values[-1] > self._tolerance)

    def inverse(self) -> np.ndarray:
        if not self.is_invertible():
            raise ValueError("matrix is singular and has no inverse")
        return np.linalg.inv(self._matrix)

    def apply(self, vector) -> np.ndarray:
        return self._matrix @ self._vector(vector, "input")

    def solve(self, output) -> np.ndarray:
        return self.inverse() @ self._vector(output, "output")

    def strongest_input_direction(self) -> np.ndarray:
        return self._vt.T[:, 0].copy()

    def weakest_input_direction(self) -> np.ndarray:
        return self._vt.T[:, -1].copy()

    def strongest_output_direction(self) -> np.ndarray:
        return self._u[:, 0].copy()

    def weakest_output_direction(self) -> np.ndarray:
        return self._u[:, -1].copy()

    def inverse_response_norm(self, lane: str, magnitude: float = 1.0) -> float:
        size = self._finite_nonnegative_scalar(magnitude)
        if lane == "strong":
            singular_value = self._singular_values[0]
        elif lane == "weak":
            singular_value = self._singular_values[-1]
        else:
            raise ValueError("lane must be 'strong' or 'weak'")
        if singular_value <= self._tolerance:
            return float("inf")
        return float(size / singular_value)

    def sensitivity_ratio(self) -> float:
        strong = self.inverse_response_norm("strong")
        weak = self.inverse_response_norm("weak")
        return float(weak / strong)

    def relative_error_ratios(self, output, perturbation) -> tuple[float, float]:
        target = self._vector(output, "output")
        delta = self._vector(perturbation, "perturbation")
        solution = self.solve(target)
        solution_delta = self.solve(delta)
        output_norm = np.linalg.norm(target)
        solution_norm = np.linalg.norm(solution)
        if output_norm == 0 or solution_norm == 0:
            raise ValueError("relative errors require nonzero output and solution")
        output_relative = float(np.linalg.norm(delta) / output_norm)
        solution_relative = float(np.linalg.norm(solution_delta) / solution_norm)
        return output_relative, solution_relative

    def satisfies_relative_error_bound(self, output, perturbation) -> bool:
        output_relative, solution_relative = self.relative_error_ratios(output, perturbation)
        return bool(solution_relative <= self.condition_number() * output_relative + 1e-12)

    @staticmethod
    def _finite_nonnegative_scalar(value: float) -> float:
        candidate = np.asarray(value, dtype=float)
        if candidate.ndim != 0 or not np.isfinite(candidate) or candidate < 0:
            raise ValueError("magnitude must be a finite nonnegative scalar")
        return float(candidate)

    @staticmethod
    def _vector(vector, name: str) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (2,):
            raise ValueError(f"{name} vector must have exactly two components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError(f"{name} vector entries must be finite")
        return candidate
