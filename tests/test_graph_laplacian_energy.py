import inspect

import numpy as np
import pytest

from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.graph_laplacian_operator import GraphLaplacianOperator


def test_default_model_uses_recurring_orders():
    model = GraphLaplacianEnergy()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.oriented_edges == ((1, 2), (2, 3), (1, 3), (3, 4))


def test_recurring_signal_has_expected_differences_and_contributions():
    model = GraphLaplacianEnergy()
    assert np.array_equal(model.edge_differences([1, 2, 3, 4]), [1, 1, 2, 1])
    assert np.array_equal(model.edge_contributions([1, 2, 3, 4]), [1, 1, 4, 1])


def test_three_energy_formulas_agree_on_exact_value_seven():
    model = GraphLaplacianEnergy()
    assert model.energy_identity([1, 2, 3, 4]) == (7.0, 7.0, 7.0)


def test_constant_signals_have_zero_energy():
    model = GraphLaplacianEnergy()
    for constant in (-3.0, 0.0, 2.5):
        values = [constant] * 4
        assert np.array_equal(model.edge_differences(values), np.zeros(4))
        assert model.energy_identity(values) == (0.0, 0.0, 0.0)


@pytest.mark.parametrize(
    "values",
    (
        (1, 0, 0, 0),
        (0, 1, -1, 2),
        (-3, -1, 4, 7),
        (0.5, -2.25, 3.75, 1.0),
    ),
)
def test_energy_is_nonnegative_because_it_is_a_sum_of_squares(values):
    model = GraphLaplacianEnergy()
    quadratic, incidence, graph_edges = model.energy_identity(values)
    assert quadratic == pytest.approx(incidence)
    assert incidence == pytest.approx(graph_edges)
    assert quadratic >= 0


@pytest.mark.parametrize("edge_number", (1, 2, 3, 4))
def test_energy_is_independent_of_single_edge_orientation_reversal(edge_number):
    values = [1, 2, 3, 4]
    model = GraphLaplacianEnergy()
    reversed_model = model.with_reversed_edge(edge_number)
    expected_differences = model.edge_differences(values).copy()
    expected_differences[edge_number - 1] *= -1
    assert np.array_equal(reversed_model.edge_differences(values), expected_differences)
    assert np.array_equal(reversed_model.edge_contributions(values), [1, 1, 4, 1])
    assert reversed_model.energy_identity(values) == (7.0, 7.0, 7.0)


def test_zero_local_laplacian_coordinate_does_not_force_zero_energy():
    laplacian = GraphLaplacianOperator()
    model = GraphLaplacianEnergy(laplacian)
    assert laplacian.apply([1, 2, 3, 4])[1] == 0
    assert model.quadratic_energy([1, 2, 3, 4]) == 7


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, np.nan, 3, 4)))
def test_invalid_values_are_rejected_by_every_energy_route(values):
    model = GraphLaplacianEnergy()
    with pytest.raises(ValueError, match="values"):
        model.quadratic_energy(values)
    with pytest.raises(ValueError, match="values"):
        model.incidence_energy(values)
    with pytest.raises(ValueError, match="values"):
        model.graph_edge_energy(values)


def test_invalid_laplacian_is_rejected():
    with pytest.raises(ValueError, match="GraphLaplacianOperator"):
        GraphLaplacianEnergy(laplacian=object())


def test_engine_composes_cp230_model_and_has_no_renderer_dependency():
    module = inspect.getmodule(GraphLaplacianEnergy)
    source = inspect.getsource(module)
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in source
    assert "from manim" not in source
    assert "import manim" not in source
