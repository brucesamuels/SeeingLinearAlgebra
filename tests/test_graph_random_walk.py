import inspect

import numpy as np
import pytest

from engine.graph_random_walk import GraphRandomWalk
from engine.simple_undirected_graph import SimpleUndirectedGraph


def test_transition_matrix_is_exact_column_stochastic_matrix():
    model = GraphRandomWalk()
    expected = np.array(
        [
            [0, 1 / 2, 1 / 3, 0],
            [1 / 2, 0, 1 / 3, 0],
            [1 / 2, 1 / 2, 0, 1],
            [0, 0, 1 / 3, 0],
        ]
    )
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.transition_matrix() == pytest.approx(expected)
    assert model.column_sums() == pytest.approx(np.ones(4))


def test_point_mass_at_vertex_four_and_exact_early_steps():
    model = GraphRandomWalk()
    p0 = model.point_mass(4)
    trajectory = model.trajectory(p0, 4)
    assert trajectory[0] == pytest.approx([0, 0, 0, 1])
    assert trajectory[1] == pytest.approx([0, 0, 1, 0])
    assert trajectory[2] == pytest.approx([1 / 3, 1 / 3, 0, 1 / 3])
    assert trajectory[3] == pytest.approx([1 / 6, 1 / 6, 2 / 3, 0])
    assert trajectory[4] == pytest.approx([11 / 36, 11 / 36, 1 / 6, 2 / 9])


def test_evolve_matches_repeated_one_step_updates():
    model = GraphRandomWalk()
    start = model.point_mass(4)
    for steps, state in enumerate(model.trajectory(start, 8)):
        assert model.evolve(start, steps) == pytest.approx(state)


def test_every_evolved_state_remains_a_probability_distribution():
    model = GraphRandomWalk()
    start = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
    for state in model.trajectory(start, 20):
        assert np.all(state >= -1e-12)
        assert state.sum() == pytest.approx(1)


def test_stationary_distribution_is_degree_proportional():
    model = GraphRandomWalk()
    assert model.encoding.degree_vector().tolist() == [2, 2, 3, 1]
    assert model.stationary_distribution() == pytest.approx([1 / 4, 1 / 4, 3 / 8, 1 / 8])
    assert model.is_stationary([1 / 4, 1 / 4, 3 / 8, 1 / 8])


def test_uniform_distribution_is_not_stationary_on_nonregular_graph():
    model = GraphRandomWalk()
    assert not model.is_stationary([1 / 4] * 4)
    assert model.next_distribution([1 / 4] * 4) == pytest.approx(
        [5 / 24, 5 / 24, 1 / 2, 1 / 12]
    )


def test_stationary_distribution_reduces_to_laplacian_null_vector():
    model = GraphRandomWalk()
    assert model.stationary_laplacian_vector() == pytest.approx([1 / 8] * 4)
    assert model.stationary_laplacian_residual() == pytest.approx(np.zeros(4))


def test_this_graph_approaches_stationarity_from_vertex_four():
    model = GraphRandomWalk()
    stationary = model.stationary_distribution()
    start = model.point_mass(4)
    assert model.total_variation_distance(model.evolve(start, 4), stationary) > 0.15
    assert model.total_variation_distance(model.evolve(start, 24), stationary) < 0.001


def test_total_variation_distance_is_symmetric_and_zero_on_equal_inputs():
    model = GraphRandomWalk()
    first = model.point_mass(1)
    second = model.point_mass(4)
    assert model.total_variation_distance(first, second) == pytest.approx(1)
    assert model.total_variation_distance(first, second) == model.total_variation_distance(second, first)
    assert model.total_variation_distance(first, first) == 0


@pytest.mark.parametrize("vertex", (0, 5, "missing"))
def test_unknown_point_mass_vertex_is_rejected(vertex):
    with pytest.raises(ValueError, match="known vertex"):
        GraphRandomWalk().point_mass(vertex)


@pytest.mark.parametrize(
    "distribution",
    (
        (1, 0, 0),
        (1, 0, 0, 0, 0),
        (0.5, 0.5, 0, np.nan),
        (1.1, -0.1, 0, 0),
        (0.2, 0.2, 0.2, 0.2),
    ),
)
def test_invalid_distributions_are_rejected(distribution):
    with pytest.raises(ValueError, match="distribution"):
        GraphRandomWalk().next_distribution(distribution)


@pytest.mark.parametrize("steps", (-1, 1.5, True))
def test_invalid_step_counts_are_rejected(steps):
    with pytest.raises(ValueError, match="nonnegative integer"):
        GraphRandomWalk().evolve([0, 0, 0, 1], steps)


def test_isolated_vertex_and_invalid_graph_are_rejected():
    with pytest.raises(ValueError, match="isolated"):
        GraphRandomWalk(SimpleUndirectedGraph((1, 2, 3), ((1, 2),)))
    with pytest.raises(ValueError, match="SimpleUndirectedGraph"):
        GraphRandomWalk(graph=object())


def test_engine_composes_graph_encoding_and_laplacian_without_renderer_dependency():
    module = inspect.getmodule(GraphRandomWalk)
    source = inspect.getsource(module)
    assert "from engine.graph_matrix_encoding import GraphMatrixEncoding" in source
    assert "from engine.graph_laplacian_operator import GraphLaplacianOperator" in source
    assert "from manim" not in source
    assert "import manim" not in source
