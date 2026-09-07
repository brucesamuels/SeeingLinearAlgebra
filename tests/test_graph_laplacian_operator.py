import inspect

import numpy as np
import pytest

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_operator import GraphLaplacianOperator


EXPECTED_L = np.array(
    [
        [2, -1, -1, 0],
        [-1, 2, -1, 0],
        [-1, -1, 3, -1],
        [0, 0, -1, 1],
    ]
)


def test_default_operator_uses_recurring_vertex_and_edge_orders():
    model = GraphLaplacianOperator()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.oriented_edges == ((1, 2), (2, 3), (1, 3), (3, 4))


def test_incidence_and_degree_adjacency_formulas_agree():
    model = GraphLaplacianOperator()
    assert np.array_equal(model.laplacian_from_incidence(), EXPECTED_L)
    assert np.array_equal(model.laplacian_from_degree_adjacency(), EXPECTED_L)
    assert np.array_equal(model.laplacian_matrix(), EXPECTED_L)


def test_vertex_to_edge_to_vertex_pipeline_matches_laplacian_action():
    model = GraphLaplacianOperator()
    edge_differences = model.edge_differences([1, 2, 3, 4])
    returned = model.return_to_vertices(edge_differences)
    assert np.array_equal(edge_differences, [1, 1, 2, 1])
    assert np.array_equal(returned, [-3, 0, 2, 1])
    assert np.array_equal(model.apply([1, 2, 3, 4]), returned)


def test_each_coordinate_is_own_value_minus_each_neighbor_value():
    model = GraphLaplacianOperator()
    expected = [-3, 0, 2, 1]
    for vertex, value in zip(model.vertex_order, expected):
        assert model.local_difference_sum(vertex, [1, 2, 3, 4]) == value


def test_constant_vertex_values_are_annihilated():
    model = GraphLaplacianOperator()
    assert np.array_equal(model.apply([1, 1, 1, 1]), np.zeros(4))
    assert np.array_equal(model.laplacian_matrix().sum(axis=1), np.zeros(4))


@pytest.mark.parametrize("edge_number", (1, 2, 3, 4))
def test_laplacian_is_independent_of_each_single_edge_reversal(edge_number):
    model = GraphLaplacianOperator()
    reversed_model = model.with_reversed_edge(edge_number)
    assert not np.array_equal(
        model.incidence.incidence_matrix(), reversed_model.incidence.incidence_matrix()
    )
    assert np.array_equal(reversed_model.laplacian_matrix(), EXPECTED_L)
    assert np.array_equal(reversed_model.apply([1, 2, 3, 4]), [-3, 0, 2, 1])


def test_transpose_accumulation_uses_signed_edge_roles():
    model = GraphLaplacianOperator()
    assert np.array_equal(model.return_to_vertices([1, 1, 2, 1]), [-3, 0, 2, 1])
    assert np.array_equal(model.return_to_vertices([0, 0, 1, 0]), [-1, 0, 1, 0])


@pytest.mark.parametrize(
    "values",
    ((1, 2, 3), (1, 2, 3, 4, 5), (1, 2, np.inf, 4)),
)
def test_invalid_vertex_values_are_rejected(values):
    model = GraphLaplacianOperator()
    with pytest.raises(ValueError, match="vertex values"):
        model.apply(values)
    with pytest.raises(ValueError, match="vertex values"):
        model.edge_differences(values)


@pytest.mark.parametrize(
    "values",
    ((1, 2, 3), (1, 2, 3, 4, 5), (1, 2, np.nan, 4)),
)
def test_invalid_edge_values_are_rejected(values):
    with pytest.raises(ValueError, match="edge values"):
        GraphLaplacianOperator().return_to_vertices(values)


def test_unknown_vertex_and_invalid_incidence_are_rejected():
    model = GraphLaplacianOperator()
    with pytest.raises(ValueError, match="known vertex"):
        model.local_difference_sum(9, [1, 2, 3, 4])
    with pytest.raises(ValueError, match="GraphIncidenceEncoding"):
        GraphLaplacianOperator(incidence=object())


def test_custom_orientation_changes_b_but_not_l():
    standard = GraphLaplacianOperator()
    reversed_incidence = GraphIncidenceEncoding(
        oriented_edges=((2, 1), (3, 2), (3, 1), (4, 3))
    )
    reversed_model = GraphLaplacianOperator(reversed_incidence)
    assert np.array_equal(
        reversed_model.incidence.incidence_matrix(),
        -standard.incidence.incidence_matrix(),
    )
    assert np.array_equal(reversed_model.laplacian_matrix(), EXPECTED_L)


def test_engine_composes_cp229_model_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphLaplacianOperator)
    source = inspect.getsource(module)
    assert "from engine.graph_incidence_encoding import GraphIncidenceEncoding" in source
    assert "from manim" not in source
    assert "import manim" not in source
