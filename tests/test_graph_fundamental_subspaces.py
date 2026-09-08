import inspect

import numpy as np
import pytest

from engine.graph_fundamental_subspaces import GraphFundamentalSubspaces


def test_recurring_incidence_matrix_and_dimensions_are_exact():
    model = GraphFundamentalSubspaces()
    expected = np.array(
        [[-1, 1, 0, 0], [0, -1, 1, 0], [-1, 0, 1, 0], [0, 0, -1, 1]]
    )
    assert model.incidence_matrix() == pytest.approx(expected)
    assert model.vertex_count == 4
    assert model.edge_count == 4
    assert model.rank == 3
    assert model.nullity == 1
    assert model.left_nullity == 1
    assert model.component_count == 1
    assert model.cycle_rank == 1


def test_null_space_records_constant_vertex_values():
    model = GraphFundamentalSubspaces()
    assert model.edge_differences([1, 1, 1, 1]) == pytest.approx(np.zeros(4))
    assert model.is_componentwise_constant([7, 7, 7, 7])
    assert not model.is_componentwise_constant([1, 1, 1, 2])
    indicators = model.component_indicators()
    assert len(indicators) == 1
    assert indicators[0] == pytest.approx([1, 1, 1, 1])


def test_row_space_is_balanced_on_the_connected_component():
    model = GraphFundamentalSubspaces()
    assert model.is_balanced_on_components([-1, 1, 0, 0])
    assert model.is_balanced_on_components([1, 1, 0, -2])
    assert not model.is_balanced_on_components([1, 0, 0, 0])


def test_column_space_contains_compatible_edge_differences():
    model = GraphFundamentalSubspaces()
    differences = model.edge_differences([1, 2, 3, 4])
    assert differences == pytest.approx([1, 1, 2, 1])
    assert model.cycle_sum(differences) == pytest.approx(0)
    assert model.is_compatible_edge_difference(differences)
    assert model.cycle_sum([1, 1, 1, 1]) == pytest.approx(1)
    assert not model.is_compatible_edge_difference([1, 1, 1, 1])


def test_left_null_space_is_triangle_circulation():
    model = GraphFundamentalSubspaces()
    circulation = model.cycle_flow()
    assert circulation == pytest.approx([1, 1, -1, 0])
    assert model.vertex_accumulation(circulation) == pytest.approx(np.zeros(4))


def test_edge_data_decomposes_into_gradient_and_circulation():
    model = GraphFundamentalSubspaces()
    edge_data = np.array([1, 1, 1, 1], dtype=float)
    gradient = model.gradient_component(edge_data)
    circulation = model.circulation_component(edge_data)
    assert gradient == pytest.approx([2 / 3, 2 / 3, 4 / 3, 1])
    assert circulation == pytest.approx([1 / 3, 1 / 3, -1 / 3, 0])
    assert gradient + circulation == pytest.approx(edge_data)
    assert model.is_compatible_edge_difference(gradient)
    assert model.vertex_accumulation(circulation) == pytest.approx(np.zeros(4), abs=1e-12)


def test_deleting_bridge_changes_components_but_not_cycle_rank():
    split = GraphFundamentalSubspaces.without_edge((3, 4))
    assert split.edge_count == 3
    assert split.rank == 2
    assert split.component_count == 2
    assert split.nullity == 2
    assert split.left_nullity == 1
    assert split.cycle_rank == 1
    assert tuple(tuple(vector) for vector in split.component_indicators()) == (
        (1.0, 1.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )
    assert split.is_componentwise_constant([5, 5, 5, -2])


def test_deleting_triangle_edge_removes_cycle_but_keeps_connectedness():
    tree = GraphFundamentalSubspaces.without_edge((1, 3))
    assert tree.edge_count == 3
    assert tree.rank == 3
    assert tree.component_count == 1
    assert tree.nullity == 1
    assert tree.left_nullity == 0
    assert tree.cycle_rank == 0


def test_laplacian_spaces_give_balanced_injection_condition():
    model = GraphFundamentalSubspaces()
    laplacian = model.laplacian_matrix()
    assert laplacian == pytest.approx(laplacian.T)
    assert laplacian @ np.ones(4) == pytest.approx(np.zeros(4))
    assert model.laplacian_output_is_reachable([-1, 0, 0, 1])
    assert not model.laplacian_output_is_reachable([1, 0, 0, 0])


def test_split_laplacian_requires_balance_on_each_component():
    split = GraphFundamentalSubspaces.without_edge((3, 4))
    assert split.laplacian_output_is_reachable([-1, 0, 1, 0])
    assert not split.laplacian_output_is_reachable([-1, 0, 0, 1])


@pytest.mark.parametrize(
    ("method", "values", "message"),
    (
        ("vertex_values", [1, 2, 3], "vertex values"),
        ("vertex_values", [1, 2, 3, np.nan], "vertex values"),
        ("edge_values", [1, 2, 3], "edge values"),
        ("edge_values", [1, 2, 3, np.inf], "edge values"),
        ("laplacian_output_is_reachable", [1, 2, 3], "vertex values"),
    ),
)
def test_invalid_vectors_are_rejected(method, values, message):
    model = GraphFundamentalSubspaces()
    with pytest.raises(ValueError, match=message):
        getattr(model, method)(values)


def test_noncanonical_graph_rejects_canonical_cycle_vector():
    tree = GraphFundamentalSubspaces.without_edge((1, 3))
    with pytest.raises(ValueError, match="canonical cycle flow"):
        tree.cycle_flow()


def test_returned_arrays_are_defensive_copies():
    model = GraphFundamentalSubspaces()
    matrix = model.incidence_matrix()
    cycle = model.cycle_flow()
    matrix[0, 0] = 99
    cycle[0] = 99
    assert model.incidence_matrix()[0, 0] == pytest.approx(-1)
    assert model.cycle_flow()[0] == pytest.approx(1)


def test_model_has_no_renderer_dependency():
    module = inspect.getmodule(GraphFundamentalSubspaces)
    source = inspect.getsource(module)
    assert "from manim" not in source
    assert "import manim" not in source
