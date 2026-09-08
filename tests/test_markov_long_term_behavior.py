import inspect

import numpy as np
import pytest

from engine.markov_long_term_behavior import MarkovLongTermBehavior


def test_four_state_mixing_matrix_is_exact_and_column_stochastic():
    model = MarkovLongTermBehavior.mixing_chain()
    expected = np.array(
        [
            [5 / 8, 1 / 8, 1 / 8, 1 / 8],
            [1 / 8, 5 / 8, 1 / 8, 1 / 8],
            [1 / 8, 1 / 8, 5 / 8, 1 / 8],
            [1 / 8, 1 / 8, 1 / 8, 5 / 8],
        ]
    )
    assert model.size == 4
    assert model.transition_matrix() == pytest.approx(expected)
    assert model.transition_matrix().sum(axis=0) == pytest.approx(np.ones(4))
    assert model.absorbing_states() == ()


def test_four_state_mixing_chain_has_unique_uniform_steady_distribution():
    model = MarkovLongTermBehavior.mixing_chain()
    steady = model.uniform_distribution()
    assert steady == pytest.approx([1 / 4] * 4)
    assert model.is_stationary(steady)
    assert model.fixed_space_dimension() == 1
    assert model.first_positive_power() == 1
    assert model.is_regular()


def test_exact_early_powers_from_state_one():
    model = MarkovLongTermBehavior.mixing_chain()
    start = model.point_mass(1)
    assert model.evolve(start, 0) == pytest.approx([1, 0, 0, 0])
    assert model.evolve(start, 1) == pytest.approx([5 / 8, 1 / 8, 1 / 8, 1 / 8])
    assert model.evolve(start, 2) == pytest.approx([7 / 16, 3 / 16, 3 / 16, 3 / 16])
    assert model.evolve(start, 3) == pytest.approx([11 / 32, 7 / 32, 7 / 32, 7 / 32])


def test_canonical_mixing_power_formula_matches_matrix_power():
    model = MarkovLongTermBehavior.mixing_chain()
    for steps in range(12):
        assert model.canonical_mixing_power(steps) == pytest.approx(
            np.linalg.matrix_power(model.transition_matrix(), steps)
        )
        assert model.canonical_mixing_distribution(steps) == pytest.approx(
            model.evolve(model.point_mass(1), steps)
        )


def test_mixing_probabilities_converge_to_uniform_steady_state():
    model = MarkovLongTermBehavior.mixing_chain()
    steady = model.uniform_distribution()
    assert model.total_variation_distance(model.canonical_mixing_distribution(12), steady) < 0.001
    assert model.total_variation_distance(model.canonical_mixing_distribution(20), steady) < 1e-6


def test_canonical_absorbing_transition_matrix_is_column_stochastic():
    model = MarkovLongTermBehavior.absorbing_chain()
    expected = np.array(
        [
            [1 / 2, 0, 0],
            [1 / 2, 1 / 2, 0],
            [0, 1 / 2, 1],
        ]
    )
    assert model.size == 3
    assert model.transition_matrix() == pytest.approx(expected)
    assert model.transition_matrix().sum(axis=0) == pytest.approx(np.ones(3))


def test_exact_absorbing_trajectory_from_state_one():
    model = MarkovLongTermBehavior.absorbing_chain()
    trajectory = model.trajectory(model.point_mass(1), 4)
    assert trajectory[0] == pytest.approx([1, 0, 0])
    assert trajectory[1] == pytest.approx([1 / 2, 1 / 2, 0])
    assert trajectory[2] == pytest.approx([1 / 4, 1 / 2, 1 / 4])
    assert trajectory[3] == pytest.approx([1 / 8, 3 / 8, 1 / 2])
    assert trajectory[4] == pytest.approx([1 / 16, 1 / 4, 11 / 16])


def test_closed_form_matches_matrix_powers():
    model = MarkovLongTermBehavior.absorbing_chain()
    start = model.point_mass(1)
    for steps in range(16):
        assert model.canonical_absorbing_distribution(steps) == pytest.approx(
            model.evolve(start, steps)
        )


def test_absorbing_state_is_stationary_and_long_run_limit():
    model = MarkovLongTermBehavior.absorbing_chain()
    absorbed = model.point_mass(3)
    assert model.absorbing_states() == (3,)
    assert model.is_absorbing_state(3)
    assert not model.is_absorbing_state(1)
    assert model.is_stationary(absorbed)
    assert model.stationary_residual(absorbed) == pytest.approx(np.zeros(3))
    assert model.total_variation_distance(model.evolve(model.point_mass(1), 30), absorbed) < 1e-6
    assert model.absorption_probabilities(model.point_mass(1)) == pytest.approx([1])


def test_alternating_chain_has_stationary_distribution_but_point_mass_oscillates():
    model = MarkovLongTermBehavior.alternating_chain()
    uniform = [1 / 2, 1 / 2]
    assert model.is_stationary(uniform)
    trajectory = model.trajectory(model.point_mass(1), 4)
    assert trajectory[0] == pytest.approx([1, 0])
    assert trajectory[1] == pytest.approx([0, 1])
    assert trajectory[2] == pytest.approx([1, 0])
    assert trajectory[3] == pytest.approx([0, 1])
    assert trajectory[4] == pytest.approx([1, 0])
    assert model.absorbing_states() == ()
    assert model.first_positive_power() is None
    assert not model.is_regular()


def test_branching_chain_has_two_absorbing_outcomes():
    model = MarkovLongTermBehavior.branching_chain()
    assert model.absorbing_states() == (3, 4)
    start = model.point_mass(1)
    assert model.evolve(start, 1) == pytest.approx([0, 1, 0, 0])
    assert model.evolve(start, 2) == pytest.approx([0, 0, 1 / 2, 1 / 2])
    assert model.absorption_probabilities(start) == pytest.approx([1 / 2, 1 / 2])
    assert model.absorption_probabilities(model.point_mass(3)) == pytest.approx([1, 0])
    assert model.fixed_space_dimension() == 2
    assert model.is_stationary([0, 0, 1 / 3, 2 / 3])
    assert not model.is_regular()


def test_regularity_search_accepts_an_explicit_power_bound():
    delayed_positive = MarkovLongTermBehavior(
        [
            [1 / 2, 1],
            [1 / 2, 0],
        ]
    )
    assert delayed_positive.first_positive_power(1) is None
    assert delayed_positive.first_positive_power(2) == 2
    assert delayed_positive.is_regular(2)


@pytest.mark.parametrize("bound", (-1, 1.5, True))
def test_regularity_search_rejects_invalid_bounds(bound):
    with pytest.raises(ValueError, match="nonnegative integer"):
        MarkovLongTermBehavior.mixing_chain().first_positive_power(bound)


def test_transition_matrix_is_returned_defensively():
    model = MarkovLongTermBehavior.absorbing_chain()
    returned = model.transition_matrix()
    returned[0, 0] = 99
    assert model.transition_matrix()[0, 0] == pytest.approx(1 / 2)


@pytest.mark.parametrize(
    "matrix",
    (
        (),
        ((1, 0, 0), (0, 1, 0)),
        ((1, 0), (0, np.nan)),
        ((1.1, 0), (-0.1, 1)),
        ((0.8, 0), (0.1, 1)),
    ),
)
def test_invalid_transition_matrices_are_rejected(matrix):
    with pytest.raises(ValueError, match="transition matrix"):
        MarkovLongTermBehavior(matrix)


@pytest.mark.parametrize(
    "distribution",
    (
        (1, 0),
        (1, 0, 0, 0),
        (0.5, 0.5, np.nan),
        (1.1, -0.1, 0),
        (0.2, 0.2, 0.2),
    ),
)
def test_invalid_distributions_are_rejected(distribution):
    with pytest.raises(ValueError, match="distribution"):
        MarkovLongTermBehavior.absorbing_chain().next_distribution(distribution)


@pytest.mark.parametrize("steps", (-1, 1.5, True))
def test_invalid_step_counts_are_rejected(steps):
    with pytest.raises(ValueError, match="nonnegative integer"):
        MarkovLongTermBehavior.absorbing_chain().evolve([1, 0, 0], steps)


@pytest.mark.parametrize("state", (0, 4, 1.5, True))
def test_invalid_states_are_rejected(state):
    with pytest.raises(ValueError, match="state"):
        MarkovLongTermBehavior.absorbing_chain().point_mass(state)


def test_canonical_formula_rejects_other_chains():
    with pytest.raises(ValueError, match="canonical absorbing chain"):
        MarkovLongTermBehavior.alternating_chain().canonical_absorbing_distribution(3)
    with pytest.raises(ValueError, match="canonical mixing chain"):
        MarkovLongTermBehavior.alternating_chain().canonical_mixing_power(3)


def test_model_has_no_renderer_dependency():
    module = inspect.getmodule(MarkovLongTermBehavior)
    source = inspect.getsource(module)
    assert "from manim" not in source
    assert "import manim" not in source
