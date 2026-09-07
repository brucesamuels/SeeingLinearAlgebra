"""Renderer-independent spectrum and spectral gap of a graph Laplacian."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


class GraphLaplacianSpectrum:
    """Compute ordered Laplacian eigenvalues and their energy quotients."""

    def __init__(self, graph: SimpleUndirectedGraph | None = None) -> None:
        self.graph = triangle_with_tail_graph() if graph is None else graph
        if not isinstance(self.graph, SimpleUndirectedGraph):
            raise ValueError("graph must be a SimpleUndirectedGraph")
        encoding = GraphMatrixEncoding(self.graph)
        incidence = GraphIncidenceEncoding(encoding)
        self.laplacian = GraphLaplacianOperator(incidence)
        self.energy = GraphLaplacianEnergy(self.laplacian)

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.laplacian.vertex_order

    def _values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return vector

    def ordered_eigenpairs(self) -> tuple[np.ndarray, np.ndarray]:
        """Return ascending eigenvalues and matching orthonormal columns."""

        values, vectors = np.linalg.eigh(self.laplacian.laplacian_matrix())
        values[np.isclose(values, 0.0, atol=1e-12, rtol=0.0)] = 0.0
        for column in range(vectors.shape[1]):
            nonzero = np.flatnonzero(np.abs(vectors[:, column]) > 1e-10)
            if nonzero.size and vectors[nonzero[0], column] < 0:
                vectors[:, column] *= -1
        return values, vectors

    def ordered_eigenvalues(self) -> np.ndarray:
        return self.ordered_eigenpairs()[0]

    def second_eigenvalue(self) -> float:
        if len(self.vertex_order) < 2:
            raise ValueError("second eigenvalue requires at least two vertices")
        return float(self.ordered_eigenvalues()[1])

    def spectral_gap(self) -> float:
        """Return lambda_2, the gap above the constant zero mode."""

        return self.second_eigenvalue()

    def second_mode(self) -> np.ndarray:
        if len(self.vertex_order) < 2:
            raise ValueError("second mode requires at least two vertices")
        return self.ordered_eigenpairs()[1][:, 1].copy()

    def zero_multiplicity(self) -> int:
        return int(np.count_nonzero(np.isclose(self.ordered_eigenvalues(), 0.0, atol=1e-10)))

    def is_connected_spectrally(self) -> bool:
        return self.zero_multiplicity() == 1

    def rayleigh_quotient(self, values: Iterable[float]) -> float:
        vector = self._values(values)
        norm_squared = float(vector @ vector)
        if np.isclose(norm_squared, 0.0, atol=1e-14, rtol=0.0):
            raise ValueError("Rayleigh quotient requires a nonzero vector")
        return self.energy.quadratic_energy(vector) / norm_squared

    def is_orthogonal_to_constants(self, values: Iterable[float]) -> bool:
        vector = self._values(values)
        return bool(np.isclose(vector.sum(), 0.0, atol=1e-12, rtol=0.0))

    def eigenpair_residual(self, eigenvalue: float, values: Iterable[float]) -> np.ndarray:
        if not np.isfinite(eigenvalue):
            raise ValueError("eigenvalue must be finite")
        vector = self._values(values)
        return self.laplacian.apply(vector) - float(eigenvalue) * vector

    def is_eigenpair(self, eigenvalue: float, values: Iterable[float]) -> bool:
        vector = self._values(values)
        if np.allclose(vector, 0.0, atol=1e-12, rtol=0.0):
            return False
        return bool(
            np.allclose(
                self.eigenpair_residual(eigenvalue, vector),
                0.0,
                atol=1e-10,
                rtol=0.0,
            )
        )
