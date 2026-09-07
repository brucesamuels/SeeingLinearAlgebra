import inspect

import numpy as np
import pytest

from engine.electrical_network_laplacian import ElectricalNetworkLaplacian
from engine.simple_undirected_graph import triangle_with_tail_graph


def test_default_network_uses_recurring_graph_and_orientations():
    model = ElectricalNetworkLaplacian()
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.oriented_edges == ((1, 2), (2, 3), (1, 3), (3, 4))


def test_source_sink_injections_follow_positive_source_convention():
    model = ElectricalNetworkLaplacian()
    assert np.array_equal(model.source_sink_injections(4, 1), [-1, 0, 0, 1])
    assert model.compatible_injections([-1, 0, 0, 1])
    assert not model.compatible_injections([0, 0, 0, 1])


def test_exact_potentials_for_unit_current_from_four_to_one():
    model = ElectricalNetworkLaplacian()
    voltage = model.solve_source_sink(4, 1)
    assert voltage == pytest.approx([0, 1 / 3, 2 / 3, 5 / 3])
    assert model.is_kirchhoff_solution(voltage, [-1, 0, 0, 1])


def test_oriented_currents_obey_ohms_law():
    model = ElectricalNetworkLaplacian()
    voltage = [0, 1 / 3, 2 / 3, 5 / 3]
    assert model.oriented_currents(voltage) == pytest.approx([-1 / 3, -1 / 3, -2 / 3, -1])
    assert model.current_on_edge(4, 3, voltage) == pytest.approx(1)
    assert model.current_on_edge(3, 1, voltage) == pytest.approx(2 / 3)
    assert model.current_on_edge(3, 2, voltage) == pytest.approx(1 / 3)
    assert model.current_on_edge(2, 1, voltage) == pytest.approx(1 / 3)


def test_internal_vertices_obey_current_conservation():
    model = ElectricalNetworkLaplacian()
    voltage = [0, 1 / 3, 2 / 3, 5 / 3]
    assert model.net_outflow(voltage) == pytest.approx([-1, 0, 0, 1])


def test_gauge_shift_changes_no_currents_or_net_outflows():
    model = ElectricalNetworkLaplacian()
    voltage = np.array([0, 1 / 3, 2 / 3, 5 / 3])
    shifted = model.gauge_shift(voltage, 7)
    assert shifted == pytest.approx(voltage + 7)
    assert model.oriented_currents(shifted) == pytest.approx(model.oriented_currents(voltage))
    assert model.net_outflow(shifted) == pytest.approx(model.net_outflow(voltage))


def test_reference_potential_selects_one_gauge_representative():
    model = ElectricalNetworkLaplacian()
    baseline = model.solve_source_sink(4, 1, reference_potential=0)
    shifted = model.solve_source_sink(4, 1, reference_potential=5)
    assert shifted == pytest.approx(baseline + 5)


def test_laplacian_energy_equals_dissipated_and_supplied_power():
    model = ElectricalNetworkLaplacian()
    voltage = model.solve_source_sink(4, 1)
    injections = model.source_sink_injections(4, 1)
    assert model.energy_balance(voltage, injections) == pytest.approx((5 / 3, 5 / 3, 5 / 3))


def test_effective_resistance_is_voltage_drop_for_unit_current():
    model = ElectricalNetworkLaplacian()
    assert model.effective_resistance(4, 1) == pytest.approx(5 / 3)
    assert model.effective_resistance(1, 4) == pytest.approx(5 / 3)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, np.nan, 3, 4)))
def test_invalid_potentials_are_rejected(values):
    with pytest.raises(ValueError, match="potentials"):
        ElectricalNetworkLaplacian().oriented_currents(values)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, np.inf, 3, 4)))
def test_invalid_injections_are_rejected(values):
    with pytest.raises(ValueError, match="injections"):
        ElectricalNetworkLaplacian().compatible_injections(values)


def test_incompatible_injections_cannot_be_solved():
    with pytest.raises(ValueError, match="sum to zero"):
        ElectricalNetworkLaplacian().solve_potentials(
            [0, 0, 0, 1], reference_vertex=1
        )


@pytest.mark.parametrize(
    ("source", "sink", "current", "message"),
    ((5, 1, 1, "known"), (1, 1, 1, "distinct"), (4, 1, 0, "positive"), (4, 1, np.inf, "positive")),
)
def test_invalid_source_sink_requests_are_rejected(source, sink, current, message):
    with pytest.raises(ValueError, match=message):
        ElectricalNetworkLaplacian().source_sink_injections(source, sink, current)


def test_invalid_reference_or_shift_is_rejected():
    model = ElectricalNetworkLaplacian()
    with pytest.raises(ValueError, match="reference_vertex"):
        model.solve_potentials([-1, 0, 0, 1], reference_vertex=5)
    with pytest.raises(ValueError, match="reference_potential"):
        model.solve_potentials([-1, 0, 0, 1], reference_vertex=1, reference_potential=np.nan)
    with pytest.raises(ValueError, match="shift"):
        model.gauge_shift([0, 1 / 3, 2 / 3, 5 / 3], np.inf)


def test_current_requires_an_existing_edge_with_known_vertices():
    model = ElectricalNetworkLaplacian()
    with pytest.raises(ValueError, match="known"):
        model.current_on_edge(1, 5, [0, 1 / 3, 2 / 3, 5 / 3])
    with pytest.raises(ValueError, match="edge"):
        model.current_on_edge(1, 4, [0, 1 / 3, 2 / 3, 5 / 3])


def test_disconnected_or_invalid_graph_is_rejected():
    with pytest.raises(ValueError, match="connected"):
        ElectricalNetworkLaplacian(triangle_with_tail_graph().without_edge((3, 4)))
    with pytest.raises(ValueError, match="SimpleUndirectedGraph"):
        ElectricalNetworkLaplacian(graph=object())


def test_engine_composes_existing_laplacian_models_and_has_no_renderer_dependency():
    module = inspect.getmodule(ElectricalNetworkLaplacian)
    source = inspect.getsource(module)
    assert "from engine.graph_laplacian_energy import GraphLaplacianEnergy" in source
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in source
    assert "from manim" not in source
    assert "import manim" not in source
