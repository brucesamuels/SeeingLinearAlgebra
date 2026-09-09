"""Renderer-independent synthesis for graphs, networks, and the Laplacian."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from engine.directed_page_rank import DirectedPageRank
from engine.electrical_network_laplacian import ElectricalNetworkLaplacian
from engine.graph_fundamental_subspaces import GraphFundamentalSubspaces
from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.graph_random_walk import GraphRandomWalk
from engine.graph_walk_counting import GraphWalkCounting
from engine.spectral_graph_partition import SpectralGraphPartition


@dataclass(frozen=True)
class GraphQuestion:
    question: str
    representation: str
    meaning: str


class GraphChapterSynthesis:
    """Collect the chapter's exact results around the recurring graph."""

    SIGNAL = np.array([1.0, 2.0, 3.0, 4.0])

    def __init__(self) -> None:
        self.encoding = GraphMatrixEncoding()
        self.walks = GraphWalkCounting(self.encoding)
        self.subspaces = GraphFundamentalSubspaces()
        self.laplacian = self.subspaces.laplacian
        self.energy = GraphLaplacianEnergy(self.laplacian)
        self.spectrum = GraphLaplacianSpectrum()
        self.partition = SpectralGraphPartition(self.spectrum)
        self.electrical = ElectricalNetworkLaplacian()
        self.random_walk = GraphRandomWalk()
        self.page_rank_model = DirectedPageRank()

    def adjacency_matrix(self) -> np.ndarray:
        return self.encoding.adjacency_matrix().copy()

    def degree_matrix(self) -> np.ndarray:
        return self.encoding.degree_matrix().copy()

    def incidence_matrix(self) -> np.ndarray:
        return self.subspaces.incidence_matrix()

    def laplacian_matrix(self) -> np.ndarray:
        return self.laplacian.laplacian_matrix().copy()

    def signal(self) -> np.ndarray:
        return self.SIGNAL.copy()

    def edge_differences(self) -> np.ndarray:
        return self.laplacian.edge_differences(self.SIGNAL)

    def laplacian_response(self) -> np.ndarray:
        return self.laplacian.apply(self.SIGNAL)

    def signal_energy(self) -> float:
        return self.energy.quadratic_energy(self.SIGNAL)

    def spectrum_values(self) -> np.ndarray:
        return self.spectrum.ordered_eigenvalues()

    def fiedler_direction(self) -> np.ndarray:
        vector = np.array([1.0, 1.0, 0.0, -2.0])
        if not self.spectrum.is_eigenpair(1.0, vector):
            raise RuntimeError("unexpected recurring-graph Fiedler direction")
        return vector

    def best_partition(self) -> tuple[tuple[object, ...], tuple[object, ...]]:
        return self.partition.best_sweep_partition()

    def best_partition_score(self) -> float:
        first, _ = self.best_partition()
        return self.partition.ratio_cut_score(first)

    def electrical_potentials(self) -> np.ndarray:
        return self.electrical.solve_source_sink(4, 1)

    def effective_resistance(self) -> float:
        return self.electrical.effective_resistance(4, 1)

    def random_walk_stationary(self) -> np.ndarray:
        return self.random_walk.stationary_distribution()

    def page_rank(self) -> np.ndarray:
        return self.page_rank_model.page_rank(0.5)

    def page_rank_order(self) -> tuple[tuple[object, ...], ...]:
        return self.page_rank_model.rank_order(0.5)

    def questions(self) -> tuple[GraphQuestion, ...]:
        return (
            GraphQuestion("Which vertices are directly connected?", "A", "adjacency"),
            GraphQuestion("How many walks have a fixed length?", "A^k", "walk counts"),
            GraphQuestion("How do values change across edges?", "B", "edge differences"),
            GraphQuestion("How does each vertex differ from its neighbors?", "L", "local variation"),
            GraphQuestion("How much variation is present overall?", "x^TLx", "energy"),
            GraphQuestion("Where are the components and cycles?", "subspaces of B", "graph structure"),
            GraphQuestion("Where is a weak separation?", "(lambda_2,v_2)", "spectral partition"),
            GraphQuestion("How do potentials drive conserved flow?", "Lv=b", "network solution"),
            GraphQuestion("How does probability move and settle?", "p_{k+1}=Pp_k", "random walk"),
            GraphQuestion("How can directed links define importance?", "Gr=r", "PageRank"),
        )
