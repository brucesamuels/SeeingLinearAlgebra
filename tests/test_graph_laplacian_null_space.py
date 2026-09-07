import inspect

import numpy as np
import pytest

from engine.graph_laplacian_null_space import GraphLaplacianNullSpace
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


def test_default_graph_is_recurring_graph_with_bridge_removed():
    model = GraphLaplacianNullSpace()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.graph.edges == ((1, 2), (2, 3), (1, 3))
    assert model.components == ((1, 2, 3), (4,))


def test_split_graph_has_exact_block_laplacian():
    model = GraphLaplacianNullSpace()
    expected = np.array(
        [[2, -1, -1, 0], [-1, 2, -1, 0], [-1, -1, 2, 0], [0, 0, 0, 0]]
    )
    assert np.array_equal(model.laplacian.laplacian_matrix(), expected)


def test_component_indicators_form_expected_basis_columns():
    model = GraphLaplacianNullSpace()
    assert np.array_equal(model.component_indicator(1), [1, 1, 1, 0])
    assert np.array_equal(model.component_indicator(2), [0, 0, 0, 1])
    assert np.array_equal(
        model.component_indicator_matrix(),
        [[1, 0], [1, 0], [1, 0], [0, 1]],
    )
    assert model.nullity == 2


@pytest.mark.parametrize("constants", ((0, 0), (2, -3), (-1.5, 4.25)))
def test_independent_component_constants_are_null_vectors(constants):
    model = GraphLaplacianNullSpace()
    signal = model.component_constant_signal(constants)
    assert np.allclose(model.apply(signal), 0)
    assert model.energy.quadratic_energy(signal) == pytest.approx(0)
    assert model.null_space_characterization(signal) == (True, True)


@pytest.mark.parametrize(
    ("values", "expected"),
    (
        ((1, 1, 1, 9), (True, True)),
        ((1, 2, 1, 9), (False, False)),
        ((0, 0, 0, 0), (True, True)),
        ((-3, -3, -3, 2), (True, True)),
    ),
)
def test_null_space_exactly_matches_componentwise_constants(values, expected):
    model = GraphLaplacianNullSpace()
    assert model.null_space_characterization(values) == expected


def test_connected_recurring_graph_has_only_one_component_indicator():
    model = GraphLaplacianNullSpace(triangle_with_tail_graph())
    assert model.components == ((1, 2, 3, 4),)
    assert model.nullity == 1
    assert np.array_equal(model.component_indicator_matrix(), [[1], [1], [1], [1]])
    assert model.null_space_characterization([7, 7, 7, 7]) == (True, True)
    assert model.null_space_characterization([7, 7, 7, 8]) == (False, False)


def test_three_components_give_three_independent_indicator_columns():
    graph = SimpleUndirectedGraph((1, 2, 3, 4), ((1, 2),))
    model = GraphLaplacianNullSpace(graph)
    assert model.components == ((1, 2), (3,), (4,))
    assert model.nullity == 3
    assert np.linalg.matrix_rank(model.component_indicator_matrix()) == 3
    assert np.array_equal(model.component_constant_signal([5, 6, 7]), [5, 5, 6, 7])


@pytest.mark.parametrize("component_number", (0, 3, -1, 1.5, True))
def test_invalid_component_number_is_rejected(component_number):
    with pytest.raises(ValueError, match="component_number"):
        GraphLaplacianNullSpace().component_indicator(component_number)


@pytest.mark.parametrize("constants", ((1,), (1, 2, 3), (1, np.nan)))
def test_invalid_component_constants_are_rejected(constants):
    with pytest.raises(ValueError, match="constants"):
        GraphLaplacianNullSpace().component_constant_signal(constants)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, 2, np.inf, 4)))
def test_invalid_vertex_values_are_rejected(values):
    model = GraphLaplacianNullSpace()
    with pytest.raises(ValueError, match="values"):
        model.is_null_vector(values)
    with pytest.raises(ValueError, match="values"):
        model.is_componentwise_constant(values)


def test_invalid_graph_is_rejected():
    with pytest.raises(ValueError, match="SimpleUndirectedGraph"):
        GraphLaplacianNullSpace(graph=object())


def test_engine_composes_existing_graph_models_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphLaplacianNullSpace)
    source = inspect.getsource(module)
    assert "from engine.graph_laplacian_energy import GraphLaplacianEnergy" in source
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in source
    assert "from manim" not in source
    assert "import manim" not in source
