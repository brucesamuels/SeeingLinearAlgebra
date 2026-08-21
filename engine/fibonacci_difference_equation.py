"""Renderer-independent mathematics for CP182: Fibonacci and difference equations."""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

FIBONACCI_MATRIX = np.array([[1.0, 1.0], [1.0, 0.0]])
PHI = (1.0 + math.sqrt(5.0)) / 2.0
PSI = (1.0 - math.sqrt(5.0)) / 2.0
P = np.array([[PHI, PSI], [1.0, 1.0]])
D = np.diag([PHI, PSI])


@dataclass(frozen=True)
class FibonacciExample:
    n: int
    fibonacci_number: int
    state: np.ndarray
    matrix_power_state: np.ndarray
    binet_value: float


class FibonacciDifferenceEquationLesson:
    """Mathematical model for solving the Fibonacci recurrence by diagonalization."""

    @property
    def matrix(self) -> np.ndarray:
        return FIBONACCI_MATRIX.copy()

    @property
    def eigenvalues(self) -> tuple[float, float]:
        return PHI, PSI

    @property
    def eigenvector_matrix(self) -> np.ndarray:
        return P.copy()

    @property
    def diagonal_matrix(self) -> np.ndarray:
        return D.copy()

    def fibonacci(self, n: int) -> int:
        if n < 0:
            raise ValueError("n must be nonnegative")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def state(self, n: int) -> np.ndarray:
        if n < 0:
            raise ValueError("n must be nonnegative")
        return np.array([float(self.fibonacci(n + 1)), float(self.fibonacci(n))])

    def matrix_power_state(self, n: int) -> np.ndarray:
        if n < 0:
            raise ValueError("n must be nonnegative")
        x0 = np.array([1.0, 0.0])
        return np.linalg.matrix_power(FIBONACCI_MATRIX, n) @ x0

    def diagonalized_power(self, n: int) -> np.ndarray:
        if n < 0:
            raise ValueError("n must be nonnegative")
        return P @ np.diag([PHI**n, PSI**n]) @ np.linalg.inv(P)

    def binet(self, n: int) -> float:
        if n < 0:
            raise ValueError("n must be nonnegative")
        return (PHI**n - PSI**n) / math.sqrt(5.0)

    def ratio(self, n: int) -> float:
        if n < 1:
            raise ValueError("n must be at least 1")
        return self.fibonacci(n + 1) / self.fibonacci(n)

    def example(self, n: int = 8) -> FibonacciExample:
        return FibonacciExample(
            n=n,
            fibonacci_number=self.fibonacci(n),
            state=self.state(n),
            matrix_power_state=self.matrix_power_state(n),
            binet_value=self.binet(n),
        )
