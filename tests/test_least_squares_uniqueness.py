import numpy as np
import pytest

from engine.least_squares_uniqueness import LeastSquaresUniqueness


def test_default_example_has_clean_normal_equations():
    model = LeastSquaresUniqueness()
    assert np.allclose(model.gram_matrix(), [[2.0, 1.0], [1.0, 2.0]])
    assert np.allclose(model.normal_right_hand_side(), [3.0, 3.0])
    assert model.has_independent_columns()
    assert model.gram_is_positive_definite()


def test_default_least_squares_solution_and_residual_are_exact():
    model = LeastSquaresUniqueness()
    solution = model.unique_solution()
    assert np.allclose(solution, [1.0, 1.0])
    assert np.allclose(model.fitted_vector(solution), [1.0, 2.0, 1.0])
    assert np.allclose(model.residual(solution), [1.0, -1.0, 1.0])
    assert np.allclose(model.normal_residual(solution), [0.0, 0.0])
    assert model.objective(solution) == pytest.approx(3.0)


def test_dependent_columns_allow_distinct_coefficients_with_same_fit():
    model = LeastSquaresUniqueness(
        [[1.0, 2.0], [1.0, 2.0], [0.0, 0.0]],
        [3.0, 3.0, 1.0],
    )
    first = np.array([3.0, 0.0])
    null_direction = np.array([-2.0, 1.0])
    second = model.shifted_coefficient(first, null_direction, 1.0)
    assert not model.has_independent_columns()
    assert not model.gram_is_positive_definite()
    assert np.allclose(second, [1.0, 1.0])
    assert np.allclose(model.fitted_vector(first), [3.0, 3.0, 0.0])
    assert np.allclose(model.fitted_vector(second), model.fitted_vector(first))
    assert model.objective(first) == pytest.approx(model.objective(second))
    with pytest.raises(ValueError, match="not unique"):
        model.unique_solution()


@pytest.mark.parametrize(
    "matrix,target",
    [([], []), ([[1.0, 2.0]], [1.0, 2.0]), ([[1.0, np.inf]], [1.0])],
)
def test_invalid_input_is_rejected(matrix, target):
    with pytest.raises(ValueError):
        LeastSquaresUniqueness(matrix, target)


def test_invalid_coefficient_and_null_direction_are_rejected():
    model = LeastSquaresUniqueness()
    with pytest.raises(ValueError, match="coefficient"):
        model.objective([1.0])
    with pytest.raises(ValueError, match="null_direction"):
        model.shifted_coefficient([1.0, 1.0], [1.0, 0.0], 2.0)
    with pytest.raises(ValueError, match="amount"):
        model.shifted_coefficient([1.0, 1.0], [0.0, 0.0], np.inf)
