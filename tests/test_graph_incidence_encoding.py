import inspect

import numpy as np
import pytest

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph


EXPECTED_B = np.array(
    [
        [-1, 1, 0, 0],
        [0, -1, 1, 0],
        [-1, 0, 1, 0],
        [0, 0, -1, 1],
    ]
)


def test_default_orientation_and_shape_use_recurring_graph_orders():
    model = GraphIncidenceEncoding()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.oriented_edges == ((1, 2), (2, 3), (1, 3), (3, 4))
    assert model.shape == (4, 4)
    assert np.array_equal(model.incidence_matrix(), EXPECTED_B)


def test_each_row_has_one_tail_and_one_head():
    matrix = GraphIncidenceEncoding().incidence_matrix()
    assert np.array_equal(np.count_nonzero(matrix == -1, axis=1), np.ones(4))
    assert np.array_equal(np.count_nonzero(matrix == 1, axis=1), np.ones(4))
    assert np.array_equal(matrix.sum(axis=1), np.zeros(4))


def test_rows_follow_the_declared_edge_order():
    model = GraphIncidenceEncoding()
    for number, expected in enumerate(EXPECTED_B, start=1):
        assert np.array_equal(model.row_for_edge(number), expected)


def test_incidence_action_returns_head_minus_tail_differences():
    model = GraphIncidenceEncoding()
    assert np.array_equal(model.edge_differences([1, 2, 3, 4]), [1, 1, 2, 1])
    assert np.array_equal(model.edge_differences([7, 7, 7, 7]), [0, 0, 0, 0])


def test_reversing_one_edge_negates_only_its_row_and_difference():
    model = GraphIncidenceEncoding()
    reversed_model = model.reverse_edge(3)
    expected = EXPECTED_B.copy()
    expected[2] *= -1
    assert reversed_model.oriented_edges[2] == (3, 1)
    assert np.array_equal(reversed_model.incidence_matrix(), expected)
    assert np.array_equal(reversed_model.edge_differences([1, 2, 3, 4]), [1, 1, -2, 1])


def test_custom_orientation_and_vertex_order_are_supported():
    graph = SimpleUndirectedGraph(("a", "b", "c"), (("a", "b"), ("b", "c")))
    encoding = GraphMatrixEncoding(graph, vertex_order=("c", "b", "a"))
    model = GraphIncidenceEncoding(encoding, (("b", "a"), ("c", "b")))
    assert model.shape == (2, 3)
    assert np.array_equal(model.incidence_matrix(), [[0, -1, 1], [-1, 1, 0]])


@pytest.mark.parametrize(
    "oriented_edges",
    (
        ((1, 2), (2, 3), (1, 3)),
        ((1, 2), (2, 3), (1, 3), (3, 4), (4, 3)),
        ((1, 2), (2, 3), (1, 3), (1, 3)),
        ((1, 2), (2, 3), (1, 4), (3, 4)),
        ((1, 2), (2, 3), (1, 3), (4, 4)),
        ((1, 2), (2, 3), (1, 3), (3,)),
    ),
)
def test_invalid_orientation_sets_are_rejected(oriented_edges):
    with pytest.raises(ValueError, match="oriented edge|oriented_edges"):
        GraphIncidenceEncoding(oriented_edges=oriented_edges)


@pytest.mark.parametrize("edge_number", (0, 5, 1.5, True))
def test_edge_numbers_are_one_based_integers(edge_number):
    model = GraphIncidenceEncoding()
    with pytest.raises(ValueError, match="edge_number"):
        model.row_for_edge(edge_number)
    with pytest.raises(ValueError, match="edge_number"):
        model.reverse_edge(edge_number)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, 2, np.inf, 4)))
def test_invalid_vertex_values_are_rejected(values):
    with pytest.raises(ValueError, match="values"):
        GraphIncidenceEncoding().edge_differences(values)


def test_invalid_encoding_is_rejected():
    with pytest.raises(ValueError, match="GraphMatrixEncoding"):
        GraphIncidenceEncoding(encoding=object())


def test_engine_composes_cp227_encoding_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphIncidenceEncoding)
    source = inspect.getsource(module)
    assert "from engine.graph_matrix_encoding import GraphMatrixEncoding" in source
    assert "from manim" not in source
    assert "import manim" not in source
