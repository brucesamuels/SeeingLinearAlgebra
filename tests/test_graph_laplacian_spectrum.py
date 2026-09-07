import inspect

import numpy as np
import pytest

from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


def test_recurring_graph_has_exact_ordered_spectrum():
    model = GraphLaplacianSpectrum()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.ordered_eigenvalues() == pytest.approx([0, 1, 3, 4], abs=1e-12)


@pytest.mark.parametrize(
    ("eigenvalue", "vector"),
    (
        (0, (1, 1, 1, 1)),
        (1, (1, 1, 0, -2)),
        (3, (1, -1, 0, 0)),
        (4, (1, 1, -3, 1)),
    ),
)
def test_exact_recurring_eigenpairs(eigenvalue, vector):
    model = GraphLaplacianSpectrum()
    assert model.is_eigenpair(eigenvalue, vector)
    assert np.array_equal(model.eigenpair_residual(eigenvalue, vector), np.zeros(4))


def test_second_mode_is_canonical_normalized_exact_direction():
    mode = GraphLaplacianSpectrum().second_mode()
    expected = np.array([1, 1, 0, -2], dtype=float) / np.sqrt(6)
    assert mode == pytest.approx(expected, abs=1e-12)


def test_spectral_gap_is_second_smallest_eigenvalue():
    model = GraphLaplacianSpectrum()
    assert model.second_eigenvalue() == pytest.approx(1)
    assert model.spectral_gap() == pytest.approx(1)


def test_second_mode_is_mean_zero_and_its_rayleigh_quotient_is_gap():
    model = GraphLaplacianSpectrum()
    vector = [1, 1, 0, -2]
    assert model.is_orthogonal_to_constants(vector)
    assert model.energy.quadratic_energy(vector) == pytest.approx(6)
    assert np.dot(vector, vector) == 6
    assert model.rayleigh_quotient(vector) == pytest.approx(model.spectral_gap())


def test_connected_graph_has_one_zero_eigenvalue():
    model = GraphLaplacianSpectrum(triangle_with_tail_graph())
    assert model.zero_multiplicity() == 1
    assert model.is_connected_spectrally()


def test_bridge_deleted_graph_has_two_zeros_and_gap_zero():
    split = triangle_with_tail_graph().without_edge((3, 4))
    model = GraphLaplacianSpectrum(split)
    assert model.ordered_eigenvalues() == pytest.approx([0, 0, 3, 3], abs=1e-12)
    assert model.zero_multiplicity() == 2
    assert model.spectral_gap() == pytest.approx(0)
    assert not model.is_connected_spectrally()


def test_spectral_connectivity_matches_graph_connectivity():
    examples = (
        triangle_with_tail_graph(),
        triangle_with_tail_graph().without_edge((3, 4)),
        SimpleUndirectedGraph((1, 2, 3), ((1, 2), (2, 3))),
        SimpleUndirectedGraph((1, 2, 3), ()),
    )
    for graph in examples:
        assert GraphLaplacianSpectrum(graph).is_connected_spectrally() == graph.is_connected()


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, np.nan, 3, 4)))
def test_invalid_values_are_rejected(values):
    model = GraphLaplacianSpectrum()
    with pytest.raises(ValueError, match="values"):
        model.rayleigh_quotient(values)
    with pytest.raises(ValueError, match="values"):
        model.is_orthogonal_to_constants(values)
    with pytest.raises(ValueError, match="values"):
        model.is_eigenpair(1, values)


def test_zero_vector_has_no_rayleigh_quotient_and_is_not_an_eigenvector():
    model = GraphLaplacianSpectrum()
    with pytest.raises(ValueError, match="nonzero"):
        model.rayleigh_quotient([0, 0, 0, 0])
    assert not model.is_eigenpair(0, [0, 0, 0, 0])


def test_invalid_eigenvalue_is_rejected():
    with pytest.raises(ValueError, match="finite"):
        GraphLaplacianSpectrum().eigenpair_residual(np.inf, [1, 1, 0, -2])


def test_second_spectral_data_require_at_least_two_vertices():
    model = GraphLaplacianSpectrum(SimpleUndirectedGraph((1,), ()))
    with pytest.raises(ValueError, match="at least two"):
        model.second_eigenvalue()
    with pytest.raises(ValueError, match="at least two"):
        model.second_mode()


def test_invalid_graph_is_rejected():
    with pytest.raises(ValueError, match="SimpleUndirectedGraph"):
        GraphLaplacianSpectrum(graph=object())


def test_engine_composes_existing_laplacian_models_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphLaplacianSpectrum)
    source = inspect.getsource(module)
    assert "from engine.graph_laplacian_energy import GraphLaplacianEnergy" in source
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in source
    assert "from manim" not in source
    assert "import manim" not in source
