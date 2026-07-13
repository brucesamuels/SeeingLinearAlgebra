"""Rank-collapse model for the Seeing Mathematics engine.

The mathematical model is intentionally independent of Manim.  A visual scene can
ask for ``matrix_at(progress)`` or ``snapshot(progress)`` and animate the returned
data without duplicating linear-algebra logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RankCollapseSnapshot:
    """State of a rank collapse at one animation progress value."""

    progress: float
    matrix: FloatArray
    singular_values: FloatArray
    rank: int
    nullity: int


class RankCollapse:
    """Continuously collapse a matrix to a chosen lower rank.

    The collapse is defined through the singular value decomposition

        A = U diag(sigma) V^T.

    The first ``target_rank`` singular values remain fixed.  Every remaining
    singular value is multiplied by ``1 - progress``.  Thus:

    - ``progress = 0`` returns the original matrix.
    - ``progress = 1`` returns the truncated-SVD matrix of ``target_rank``.
    - intermediate values give a continuous geometric collapse.

    Parameters
    ----------
    matrix:
        Any finite, nonempty, two-dimensional real array.
    target_rank:
        Desired rank at the end of the collapse.  It must satisfy
        ``0 <= target_rank <= initial_rank``.
    tolerance:
        Numerical threshold used to decide whether a singular value is nonzero.
        When omitted, the standard matrix-rank scale
        ``max(m, n) * eps * largest_singular_value`` is used.
    """

    def __init__(
        self,
        matrix: ArrayLike,
        target_rank: int,
        *,
        tolerance: float | None = None,
    ) -> None:
        array = np.asarray(matrix, dtype=float)

        if array.ndim != 2:
            raise ValueError("matrix must be two-dimensional")
        if array.shape[0] == 0 or array.shape[1] == 0:
            raise ValueError("matrix must be nonempty")
        if not np.all(np.isfinite(array)):
            raise ValueError("matrix entries must be finite")
        if isinstance(target_rank, bool) or not isinstance(target_rank, (int, np.integer)):
            raise TypeError("target_rank must be an integer")

        # Full matrices preserve all right-singular directions, including the
        # automatic null-space directions of a wide matrix.
        u, singular_values, vh = np.linalg.svd(array, full_matrices=True)

        if tolerance is None:
            largest = float(singular_values[0]) if singular_values.size else 0.0
            tolerance_value = (
                max(array.shape) * np.finfo(float).eps * largest
            )
        else:
            if isinstance(tolerance, bool) or not isinstance(tolerance, Real):
                raise TypeError("tolerance must be a nonnegative real number")
            tolerance_value = float(tolerance)
            if not np.isfinite(tolerance_value) or tolerance_value < 0:
                raise ValueError("tolerance must be a finite nonnegative number")

        initial_rank = int(np.count_nonzero(singular_values > tolerance_value))
        target_rank_value = int(target_rank)
        if not 0 <= target_rank_value <= initial_rank:
            raise ValueError(
                "target_rank must satisfy "
                f"0 <= target_rank <= initial_rank ({initial_rank})"
            )

        # Store private immutable copies.  Public array-returning methods also
        # return copies so callers cannot mutate the model accidentally.
        self._matrix = array.copy()
        self._u = u.copy()
        self._singular_values = singular_values.copy()
        self._vh = vh.copy()
        self._target_rank = target_rank_value
        self._initial_rank = initial_rank
        self._tolerance = tolerance_value

    @property
    def shape(self) -> tuple[int, int]:
        return self._matrix.shape

    @property
    def codomain_dimension(self) -> int:
        return self.shape[0]

    @property
    def domain_dimension(self) -> int:
        return self.shape[1]

    @property
    def initial_rank(self) -> int:
        return self._initial_rank

    @property
    def target_rank(self) -> int:
        return self._target_rank

    @property
    def initial_nullity(self) -> int:
        return self.domain_dimension - self.initial_rank

    @property
    def final_nullity(self) -> int:
        return self.domain_dimension - self.target_rank

    @property
    def tolerance(self) -> float:
        return self._tolerance

    @property
    def original_matrix(self) -> FloatArray:
        return self._matrix.copy()

    def singular_values_at(self, progress: float) -> FloatArray:
        """Return the singular values at ``progress`` in the interval [0, 1]."""

        p = self._validate_progress(progress)
        values = self._singular_values.copy()
        values[self.target_rank :] *= 1.0 - p
        return values

    def matrix_at(self, progress: float) -> FloatArray:
        """Return the matrix at ``progress`` in the interval [0, 1]."""

        values = self.singular_values_at(progress)
        k = values.size
        return (self._u[:, :k] * values) @ self._vh[:k, :]

    def apply(self, vector: ArrayLike, progress: float = 1.0) -> FloatArray:
        """Apply the matrix at ``progress`` to one vector."""

        components = np.asarray(vector, dtype=float)
        if components.ndim != 1:
            raise ValueError("vector must be one-dimensional")
        if components.size != self.domain_dimension:
            raise ValueError(
                "vector dimension must equal the matrix domain dimension "
                f"({self.domain_dimension})"
            )
        if not np.all(np.isfinite(components)):
            raise ValueError("vector entries must be finite")
        return self.matrix_at(progress) @ components

    def rank_at(self, progress: float) -> int:
        """Return the numerical rank at ``progress``."""

        values = self.singular_values_at(progress)
        return int(np.count_nonzero(values > self.tolerance))

    def nullity_at(self, progress: float) -> int:
        """Return the nullity at ``progress``."""

        return self.domain_dimension - self.rank_at(progress)

    def image_basis(self, progress: float = 1.0) -> FloatArray:
        """Return an orthonormal basis for the image as matrix columns."""

        values = self.singular_values_at(progress)
        indices = np.flatnonzero(values > self.tolerance)
        return self._u[:, indices].copy()

    def row_space_basis(self, progress: float = 1.0) -> FloatArray:
        """Return an orthonormal basis for the row space as matrix rows."""

        values = self.singular_values_at(progress)
        indices = np.flatnonzero(values > self.tolerance)
        return self._vh[indices, :].copy()

    def kernel_basis(self, progress: float = 1.0) -> FloatArray:
        """Return an orthonormal basis for the kernel as matrix columns."""

        values = self.singular_values_at(progress)
        k = values.size

        zero_indices = list(np.flatnonzero(values <= self.tolerance))
        # For a wide m-by-n matrix, V^T has n rows but only min(m, n)
        # singular values.  The remaining right-singular vectors are always in
        # the kernel.
        zero_indices.extend(range(k, self.domain_dimension))

        if not zero_indices:
            return np.empty((self.domain_dimension, 0), dtype=float)

        return self._vh[zero_indices, :].T.copy()

    def snapshot(self, progress: float) -> RankCollapseSnapshot:
        """Return all primary mathematical data for one animation frame."""

        p = self._validate_progress(progress)
        values = self.singular_values_at(p)
        rank = int(np.count_nonzero(values > self.tolerance))
        return RankCollapseSnapshot(
            progress=p,
            matrix=self.matrix_at(p),
            singular_values=values,
            rank=rank,
            nullity=self.domain_dimension - rank,
        )

    def _validate_progress(self, progress: Any) -> float:
        if isinstance(progress, bool) or not isinstance(progress, Real):
            raise TypeError("progress must be a real number")
        value = float(progress)
        if not np.isfinite(value):
            raise ValueError("progress must be finite")
        if not 0.0 <= value <= 1.0:
            raise ValueError("progress must lie in the interval [0, 1]")
        return value
