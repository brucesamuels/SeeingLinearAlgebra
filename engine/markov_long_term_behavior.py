"""Renderer-independent finite Markov-chain long-term behavior model."""

from __future__ import annotations

from collections.abc import Iterable
from numbers import Integral

import numpy as np


class MarkovLongTermBehavior:
    """Evolve column distributions and identify absorbing states."""

    MIXING_CHAIN = np.full((4, 4), 1 / 8, dtype=float) + np.eye(4) / 2
    ABSORBING_CHAIN = np.array(
        [
            [1 / 2, 0, 0],
            [1 / 2, 1 / 2, 0],
            [0, 1 / 2, 1],
        ],
        dtype=float,
    )
    ALTERNATING_CHAIN = np.array([[0, 1], [1, 0]], dtype=float)
    BRANCHING_CHAIN = np.array(
        [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1 / 2, 1, 0],
            [0, 1 / 2, 0, 1],
        ],
        dtype=float,
    )

    def __init__(self, transition_matrix: Iterable[Iterable[float]]) -> None:
        matrix = np.asarray(tuple(tuple(row) for row in transition_matrix), dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("transition matrix must be nonempty and square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("transition matrix must be finite")
        if np.any(matrix < -1e-12):
            raise ValueError("transition matrix entries must be nonnegative")
        if not np.allclose(matrix.sum(axis=0), np.ones(matrix.shape[1]), atol=1e-12, rtol=0.0):
            raise ValueError("transition matrix columns must sum to one")
        matrix[np.isclose(matrix, 0.0, atol=1e-12, rtol=0.0)] = 0.0
        self._transition = matrix

    @classmethod
    def absorbing_chain(cls) -> "MarkovLongTermBehavior":
        return cls(cls.ABSORBING_CHAIN)

    @classmethod
    def mixing_chain(cls) -> "MarkovLongTermBehavior":
        return cls(cls.MIXING_CHAIN)

    @classmethod
    def alternating_chain(cls) -> "MarkovLongTermBehavior":
        return cls(cls.ALTERNATING_CHAIN)

    @classmethod
    def branching_chain(cls) -> "MarkovLongTermBehavior":
        return cls(cls.BRANCHING_CHAIN)

    @property
    def size(self) -> int:
        return self._transition.shape[0]

    def transition_matrix(self) -> np.ndarray:
        return self._transition.copy()

    @staticmethod
    def _steps(steps: int) -> int:
        if isinstance(steps, bool) or not isinstance(steps, Integral) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        return int(steps)

    def _distribution(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (self.size,)
        if vector.shape != expected:
            raise ValueError(f"distribution must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("distribution must be finite")
        if np.any(vector < -1e-12):
            raise ValueError("distribution entries must be nonnegative")
        if not np.isclose(vector.sum(), 1.0, atol=1e-12, rtol=0.0):
            raise ValueError("distribution entries must sum to one")
        vector[np.isclose(vector, 0.0, atol=1e-12, rtol=0.0)] = 0.0
        return vector

    def point_mass(self, state: int) -> np.ndarray:
        if isinstance(state, bool) or not isinstance(state, Integral) or not 1 <= state <= self.size:
            raise ValueError("state must be between 1 and the chain size")
        vector = np.zeros(self.size)
        vector[int(state) - 1] = 1.0
        return vector

    def uniform_distribution(self) -> np.ndarray:
        return np.full(self.size, 1.0 / self.size)

    def next_distribution(self, distribution: Iterable[float]) -> np.ndarray:
        return self._transition @ self._distribution(distribution)

    def evolve(self, distribution: Iterable[float], steps: int) -> np.ndarray:
        return np.linalg.matrix_power(self._transition, self._steps(steps)) @ self._distribution(distribution)

    def trajectory(
        self,
        distribution: Iterable[float],
        steps: int,
    ) -> tuple[np.ndarray, ...]:
        count = self._steps(steps)
        states = [self._distribution(distribution)]
        for _ in range(count):
            states.append(self.next_distribution(states[-1]))
        return tuple(state.copy() for state in states)

    def stationary_residual(self, distribution: Iterable[float]) -> np.ndarray:
        vector = self._distribution(distribution)
        return self._transition @ vector - vector

    def is_stationary(self, distribution: Iterable[float]) -> bool:
        return bool(np.allclose(self.stationary_residual(distribution), np.zeros(self.size)))

    def absorbing_states(self) -> tuple[int, ...]:
        absorbing = []
        for column in range(self.size):
            point_mass = self.point_mass(column + 1)
            if np.allclose(self._transition[:, column], point_mass, atol=1e-12, rtol=0.0):
                absorbing.append(column + 1)
        return tuple(absorbing)

    def is_absorbing_state(self, state: int) -> bool:
        self.point_mass(state)
        return int(state) in self.absorbing_states()

    def fixed_space_dimension(self) -> int:
        return self.size - int(np.linalg.matrix_rank(self._transition - np.eye(self.size)))

    def first_positive_power(self, max_power: int | None = None) -> int | None:
        """Return the first tested power whose entries are all positive.

        A transition matrix is regular when such a power exists.  The optional
        bound keeps the numerical test explicit; the default is the classical
        finite bound for a primitive matrix of this size.
        """

        if max_power is None:
            max_power = (self.size - 1) ** 2 + 1
        bound = self._steps(max_power)
        power = np.eye(self.size)
        for exponent in range(1, bound + 1):
            power = self._transition @ power
            if np.all(power > 1e-12):
                return exponent
        return None

    def is_regular(self, max_power: int | None = None) -> bool:
        """Return whether a positive power is found within the tested bound."""

        return self.first_positive_power(max_power) is not None

    def canonical_mixing_power(self, steps: int) -> np.ndarray:
        """Return A^k for the designated four-state convergent example."""

        if self._transition.shape != self.MIXING_CHAIN.shape or not np.allclose(
            self._transition, self.MIXING_CHAIN
        ):
            raise ValueError("power formula belongs to the canonical mixing chain")
        count = self._steps(steps)
        uniform_projection = np.full((4, 4), 1 / 4)
        return uniform_projection + (0.5**count) * (np.eye(4) - uniform_projection)

    def canonical_mixing_distribution(self, steps: int) -> np.ndarray:
        """Return A^k e_1 for the designated four-state convergent example."""

        return self.canonical_mixing_power(steps) @ self.point_mass(1)

    def canonical_absorbing_distribution(self, steps: int) -> np.ndarray:
        """Return the exact closed form for the designated three-state example."""

        if self._transition.shape != self.ABSORBING_CHAIN.shape or not np.allclose(
            self._transition, self.ABSORBING_CHAIN
        ):
            raise ValueError("closed form belongs to the canonical absorbing chain")
        count = self._steps(steps)
        power = 2.0**count
        return np.array([1 / power, count / power, 1 - (count + 1) / power])

    def absorption_probabilities(
        self,
        distribution: Iterable[float],
        steps: int = 200,
    ) -> np.ndarray:
        """Approximate eventual mass at absorbing states after many steps."""

        state = self.evolve(distribution, self._steps(steps))
        return np.array([state[index - 1] for index in self.absorbing_states()])

    def total_variation_distance(
        self,
        first: Iterable[float],
        second: Iterable[float],
    ) -> float:
        left = self._distribution(first)
        right = self._distribution(second)
        return 0.5 * float(np.abs(left - right).sum())
