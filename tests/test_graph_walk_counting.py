import inspect

import numpy as np
import pytest

from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.graph_walk_counting import GraphWalkCounting


EXPECTED_A2 = np.array(
    [
        [2, 1, 1, 1],
        [1, 2, 1, 1],
        [1, 1, 3, 0],
        [1, 1, 0, 1],
    ]
)

EXPECTED_A3 = np.array(
    [
        [2, 3, 4, 1],
        [3, 2, 4, 1],
        [4, 4, 2, 3],
        [1, 1, 3, 0],
    ]
)


def test_default_model_uses_recurring_graph_and_order():
    model = GraphWalkCounting()
    assert model.vertex_order == (1, 2, 3, 4)
    assert np.array_equal(model.matrix_power(1), model.encoding.adjacency_matrix())


def test_zero_power_counts_length_zero_walks():
    model = GraphWalkCounting()
    assert np.array_equal(model.matrix_power(0), np.eye(4, dtype=int))
    assert model.walk_count(1, 1, 0) == 1
    assert model.walk_count(1, 2, 0) == 0


def test_second_and_third_powers_have_exact_integer_counts():
    model = GraphWalkCounting()
    assert np.array_equal(model.matrix_power(2), EXPECTED_A2)
    assert np.array_equal(model.matrix_power(3), EXPECTED_A3)


def test_two_step_examples_include_returns_and_a_tail_walk():
    model = GraphWalkCounting()
    assert model.walk_count(1, 1, 2) == 2
    assert model.walks(1, 1, 2) == ((1, 2, 1), (1, 3, 1))
    assert model.walk_count(1, 4, 2) == 1
    assert model.walks(1, 4, 2) == ((1, 3, 4),)


def test_repeated_vertices_are_allowed_because_the_objects_are_walks():
    model = GraphWalkCounting()
    routes = model.walks(1, 3, 3)
    assert routes == (
        (1, 2, 1, 3),
        (1, 3, 1, 3),
        (1, 3, 2, 3),
        (1, 3, 4, 3),
    )
    assert len(routes) == model.walk_count(1, 3, 3) == 4


def test_endpoint_counts_are_one_row_of_the_matrix_power():
    model = GraphWalkCounting()
    assert np.array_equal(model.endpoint_counts(1, 0), [1, 0, 0, 0])
    assert np.array_equal(model.endpoint_counts(1, 1), [0, 1, 1, 0])
    assert np.array_equal(model.endpoint_counts(1, 2), [2, 1, 1, 1])


@pytest.mark.parametrize("length", (-1, 1.5, True))
def test_walk_length_must_be_a_nonnegative_integer(length):
    model = GraphWalkCounting()
    with pytest.raises(ValueError, match="nonnegative integer"):
        model.matrix_power(length)
    with pytest.raises(ValueError, match="nonnegative integer"):
        model.walks(1, 2, length)


def test_unknown_vertices_and_invalid_encoding_are_rejected():
    model = GraphWalkCounting()
    with pytest.raises(ValueError, match="known vertices"):
        model.walk_count(9, 1, 2)
    with pytest.raises(ValueError, match="known vertices"):
        model.walks(1, 9, 2)
    with pytest.raises(ValueError, match="GraphMatrixEncoding"):
        GraphWalkCounting(encoding=object())


def test_custom_vertex_order_is_preserved():
    model = GraphWalkCounting(GraphMatrixEncoding(vertex_order=(4, 3, 2, 1)))
    assert model.vertex_order == (4, 3, 2, 1)
    assert np.array_equal(model.endpoint_counts(1, 2), [1, 1, 1, 2])


def test_engine_composes_matrix_encoding_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphWalkCounting)
    source = inspect.getsource(module)
    assert "from engine.graph_matrix_encoding import GraphMatrixEncoding" in source
    assert "from manim" not in source
    assert "import manim" not in source
