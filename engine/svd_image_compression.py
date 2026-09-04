"""Renderer-independent grayscale image compression with truncated SVD."""

from __future__ import annotations

from numbers import Integral

import numpy as np

from engine.truncated_svd_approximation import TruncatedSVDApproximation


class SVDImageCompression:
    """Treat a grayscale image as a matrix and expose rank/storage tradeoffs."""

    def __init__(self, image=None) -> None:
        if image is None:
            image = self.synthetic_landscape()
        candidate = np.asarray(image, dtype=float)
        if candidate.ndim != 2 or not candidate.shape[0] or not candidate.shape[1]:
            raise ValueError("image must be a nonempty two-dimensional array")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("image entries must be finite")
        if np.any(candidate < 0) or np.any(candidate > 1):
            raise ValueError("image entries must lie between zero and one")
        if np.linalg.norm(candidate, ord="fro") == 0:
            raise ValueError("image must contain nonzero brightness")
        self._image = candidate.copy()
        self._approximation = TruncatedSVDApproximation(self._image)

    @staticmethod
    def synthetic_landscape(size: int = 32) -> np.ndarray:
        if not isinstance(size, Integral) or isinstance(size, bool) or size < 8:
            raise ValueError("size must be an integer at least 8")
        axis = np.linspace(0.0, 1.0, int(size))
        x, y = np.meshgrid(axis, axis)

        image = 0.82 - 0.34 * y
        sun = np.exp(-((x - 0.76) ** 2 + (y - 0.21) ** 2) / 0.006)
        image += 0.16 * sun

        far_ridge = 0.48 + 0.34 * np.abs(x - 0.70)
        far_mountain = (y >= far_ridge) & (y < 0.72)
        image[far_mountain] = 0.43 + 0.05 * x[far_mountain]

        near_ridge = 0.40 + 0.52 * np.abs(x - 0.34)
        near_mountain = (y >= near_ridge) & (y < 0.73)
        image[near_mountain] = 0.27 + 0.06 * y[near_mountain]

        ground = y >= 0.72
        image[ground] = 0.19 + 0.07 * x[ground] + 0.025 * np.cos(8 * np.pi * x[ground])

        trunk = (np.abs(x - 0.16) < 0.018) & (y > 0.52) & (y < 0.88)
        image[trunk] = 0.08
        canopy = ((x - 0.16) ** 2 / 0.010 + (y - 0.49) ** 2 / 0.030) < 1
        image[canopy] = 0.12

        reflection = np.exp(-((x - 0.76) ** 2) / 0.020) * np.exp(-((y - 0.80) ** 2) / 0.018)
        image += 0.07 * reflection
        return np.clip(image, 0.0, 1.0)

    @property
    def shape(self) -> tuple[int, int]:
        return self._image.shape

    @property
    def maximum_rank(self) -> int:
        return self._approximation.maximum_rank

    def original(self) -> np.ndarray:
        return self._image.copy()

    def singular_values(self) -> np.ndarray:
        return self._approximation.singular_values()

    def reconstruction(self, rank: int, *, clip: bool = False) -> np.ndarray:
        result = self._approximation.truncated(self._rank(rank))
        return np.clip(result, 0.0, 1.0) if clip else result

    def frobenius_error(self, rank: int) -> float:
        return self._approximation.frobenius_error(self._rank(rank))

    def relative_frobenius_error(self, rank: int) -> float:
        return float(self.frobenius_error(rank) / np.linalg.norm(self._image, ord="fro"))

    def retained_energy(self, rank: int) -> float:
        count = self._rank(rank)
        values = self.singular_values()
        return float(np.sum(values[:count] ** 2) / np.sum(values**2))

    def original_storage(self) -> int:
        rows, columns = self.shape
        return rows * columns

    def compressed_storage(self, rank: int) -> int:
        count = self._positive_rank(rank)
        rows, columns = self.shape
        return count * (rows + columns + 1)

    def storage_fraction(self, rank: int) -> float:
        return float(self.compressed_storage(rank) / self.original_storage())

    def compression_ratio(self, rank: int) -> float:
        return float(self.original_storage() / self.compressed_storage(rank))

    def _positive_rank(self, rank: int) -> int:
        count = self._rank(rank)
        if count == 0:
            raise ValueError("storage rank must be positive")
        return count

    def _rank(self, rank: int) -> int:
        if not isinstance(rank, Integral) or isinstance(rank, bool):
            raise ValueError("rank must be an integer")
        count = int(rank)
        if count < 0 or count > self.maximum_rank:
            raise ValueError(f"rank must lie between 0 and {self.maximum_rank}")
        return count
