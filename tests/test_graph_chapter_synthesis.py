import inspect

import numpy as np
import pytest

from engine.graph_chapter_synthesis import GraphChapterSynthesis


def test_recurring_graph_matrices_are_reassembled_exactly():
    model = GraphChapterSynthesis()
    assert model.adjacency_matrix() == pytest.approx(
        np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]])
    )
    assert model.degree_matrix() == pytest.approx(np.diag([2, 2, 3, 1]))
    assert model.incidence_matrix() == pytest.approx(
        np.array([[-1, 1, 0, 0], [0, -1, 1, 0], [-1, 0, 1, 0], [0, 0, -1, 1]])
    )
    assert model.laplacian_matrix() == pytest.approx(
        np.array([[2, -1, -1, 0], [-1, 2, -1, 0], [-1, -1, 3, -1], [0, 0, -1, 1]])
    )


def test_signal_reassembles_differences_response_and_energy():
    model = GraphChapterSynthesis()
    assert model.signal() == pytest.approx([1, 2, 3, 4])
    assert model.edge_differences() == pytest.approx([1, 1, 2, 1])
    assert model.laplacian_response() == pytest.approx([-3, 0, 2, 1])
    assert model.signal_energy() == pytest.approx(7)


def test_spectrum_partition_and_subspace_counts_match_graph_structure():
    model = GraphChapterSynthesis()
    assert model.spectrum_values() == pytest.approx([0, 1, 3, 4])
    assert model.fiedler_direction() == pytest.approx([1, 1, 0, -2])
    first, second = model.best_partition()
    assert {frozenset(first), frozenset(second)} == {frozenset({4}), frozenset({1, 2, 3})}
    assert model.best_partition_score() == pytest.approx(4 / 3)
    assert model.subspaces.component_count == 1
    assert model.subspaces.cycle_rank == 1


def test_electrical_and_probability_applications_retain_exact_anchors():
    model = GraphChapterSynthesis()
    assert model.electrical_potentials() == pytest.approx([0, 1 / 3, 2 / 3, 5 / 3])
    assert model.effective_resistance() == pytest.approx(5 / 3)
    assert model.random_walk_stationary() == pytest.approx([1 / 4, 1 / 4, 3 / 8, 1 / 8])
    assert model.page_rank() == pytest.approx([11 / 49, 13 / 49, 2 / 7, 11 / 49])
    assert model.page_rank_order() == ((3,), (2,), (1, 4))


def test_question_guide_covers_the_chapter_without_adding_a_new_topic():
    questions = GraphChapterSynthesis().questions()
    assert len(questions) == 10
    assert [item.representation for item in questions] == [
        "A", "A^k", "B", "L", "x^TLx", "subspaces of B",
        "(lambda_2,v_2)", "Lv=b", "p_{k+1}=Pp_k", "Gr=r",
    ]
    assert all(item.question and item.meaning for item in questions)


def test_engine_composes_existing_graph_models_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(GraphChapterSynthesis))
    for name in (
        "GraphMatrixEncoding", "GraphWalkCounting", "GraphFundamentalSubspaces",
        "GraphLaplacianEnergy", "GraphLaplacianSpectrum", "SpectralGraphPartition",
        "ElectricalNetworkLaplacian", "GraphRandomWalk", "DirectedPageRank",
    ):
        assert name in source
    assert "from manim" not in source
    assert "import manim" not in source
