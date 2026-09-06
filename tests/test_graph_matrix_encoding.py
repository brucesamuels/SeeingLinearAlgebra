import inspect

import numpy as np
import pytest

from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph


EXPECTED_ADJACENCY = np.array(
    [
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
    ]
)


def test_default_encoding_uses_recurring_graph_and_vertex_order():
    encoding = GraphMatrixEncoding()
    assert encoding.vertex_order == (1, 2, 3, 4)
    assert np.array_equal(encoding.adjacency_matrix(), EXPECTED_ADJACENCY)


def test_adjacency_matrix_is_symmetric_with_zero_diagonal():
    matrix = GraphMatrixEncoding().adjacency_matrix()
    assert np.array_equal(matrix, matrix.T)
    assert np.array_equal(np.diag(matrix), np.zeros(4))


def test_entries_encode_edges_and_non_edges():
    encoding = GraphMatrixEncoding()
    assert encoding.adjacency_entry(1, 3) == 1
    assert encoding.adjacency_entry(3, 1) == 1
    assert encoding.adjacency_entry(1, 4) == 0
    assert encoding.adjacency_entry(2, 2) == 0
    with pytest.raises(ValueError, match="known vertices"):
        encoding.adjacency_entry(1, 9)


def test_row_sums_and_degree_matrix_encode_degrees():
    encoding = GraphMatrixEncoding()
    assert np.array_equal(encoding.row_sums(), [2, 2, 3, 1])
    assert np.array_equal(encoding.degree_vector(), [2, 2, 3, 1])
    assert np.array_equal(encoding.degree_matrix(), np.diag([2, 2, 3, 1]))
    assert np.array_equal(encoding.adjacency_matrix() @ np.ones(4), [2, 2, 3, 1])


def test_matrix_vector_product_adds_neighbor_values():
    encoding = GraphMatrixEncoding()
    assert np.array_equal(encoding.neighbor_sums([1, 2, 3, 4]), [5, 4, 7, 3])


def test_reordering_vertices_changes_array_positions_but_not_graph_relations():
    encoding = GraphMatrixEncoding(vertex_order=(4, 3, 2, 1))
    expected = EXPECTED_ADJACENCY[::-1, ::-1]
    assert encoding.vertex_order == (4, 3, 2, 1)
    assert np.array_equal(encoding.adjacency_matrix(), expected)
    assert np.array_equal(encoding.degree_vector(), [1, 3, 2, 2])


@pytest.mark.parametrize("order", ((1, 2, 3), (1, 2, 3, 3), (1, 2, 3, 9)))
def test_invalid_vertex_orders_are_rejected(order):
    with pytest.raises(ValueError, match="vertex_order"):
        GraphMatrixEncoding(vertex_order=order)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, 2, np.inf, 4)))
def test_invalid_vertex_values_are_rejected(values):
    with pytest.raises(ValueError, match="values"):
        GraphMatrixEncoding().neighbor_sums(values)


def test_model_requires_simple_undirected_graph():
    with pytest.raises(ValueError, match="SimpleUndirectedGraph"):
        GraphMatrixEncoding(graph=object())
    custom = SimpleUndirectedGraph(("a", "b"), (("a", "b"),))
    assert np.array_equal(GraphMatrixEncoding(custom).adjacency_matrix(), [[0, 1], [1, 0]])


def test_engine_composes_graph_model_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphMatrixEncoding)
    source = inspect.getsource(module)
    assert "from engine.simple_undirected_graph import" in source
    assert "from manim" not in source
    assert "import manim" not in source
