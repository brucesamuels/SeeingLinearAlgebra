from __future__ import annotations

import numpy as np
import pytest

from engine.coefficient_choreography import (
    CoefficientChoreography,
    golden_ratio_coefficient_samples,
    selected_story_coefficients,
    serpentine_coefficient_grid,
)
from engine.linear_combination import LinearCombination


def test_story_coefficients_are_deterministic_and_two_dimensional() -> None:
    choices = selected_story_coefficients()

    assert len(choices) == 6
    assert all(choice.shape == (2,) for choice in choices)
    assert np.allclose(choices[0], (2.0, 1.0))
    assert np.allclose(choices[-1], (1.5, 1.25))


def test_serpentine_grid_has_expected_size_and_reverses_rows() -> None:
    grid = serpentine_coefficient_grid(
        a_min=-1.0,
        a_max=1.0,
        b_min=-1.0,
        b_max=1.0,
        a_count=3,
        b_count=3,
    )

    assert len(grid) == 9
    assert np.allclose(grid[:3], ((-1, -1), (0, -1), (1, -1)))
    assert np.allclose(grid[3:6], ((1, 0), (0, 0), (-1, 0)))


def test_choreography_delegates_to_linear_combination() -> None:
    evaluator = LinearCombination(((2.0, 0.5), (0.5, 1.5)))
    choreography = CoefficientChoreography(
        evaluator,
        ((2.0, 1.0), (-1.0, 2.0)),
    )

    first, second = choreography.samples

    assert np.allclose(first.snapshot.result, (4.5, 2.5))
    assert np.allclose(second.snapshot.result, (-1.0, 2.5))


def test_choreography_requires_at_least_one_choice() -> None:
    with pytest.raises(ValueError, match="at least one"):
        CoefficientChoreography(
            LinearCombination(((1.0, 0.0), (0.0, 1.0))),
            (),
        )


def test_grid_rejects_invalid_counts_and_limits() -> None:
    with pytest.raises(ValueError, match="at least two"):
        serpentine_coefficient_grid(
            a_min=-1,
            a_max=1,
            b_min=-1,
            b_max=1,
            a_count=1,
            b_count=3,
        )

    with pytest.raises(ValueError, match="minimum"):
        serpentine_coefficient_grid(
            a_min=1,
            a_max=-1,
            b_min=-1,
            b_max=1,
            a_count=3,
            b_count=3,
        )



def test_golden_ratio_samples_are_deterministic_and_not_gridded() -> None:
    first = golden_ratio_coefficient_samples(
        count=12,
        a_min=-2.0,
        a_max=2.0,
        b_min=-3.0,
        b_max=3.0,
    )
    second = golden_ratio_coefficient_samples(
        count=12,
        a_min=-2.0,
        a_max=2.0,
        b_min=-3.0,
        b_max=3.0,
    )

    assert len(first) == 12
    assert all(np.allclose(a, b) for a, b in zip(first, second))
    assert len({round(float(pair[0]), 10) for pair in first}) == 12
    assert len({round(float(pair[1]), 10) for pair in first}) == 12
