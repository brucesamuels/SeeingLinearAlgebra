import numpy as np
import pytest

from engine.positive_definite_elimination_test import PositiveDefiniteEliminationTest


def test_default_matrix_has_expected_pivots_and_leading_minors():
    model = PositiveDefiniteEliminationTest()
    np.testing.assert_allclose(model.elimination_pivots(), [2.0, 1.5])
    np.testing.assert_allclose(model.leading_principal_minors(), [2.0, 3.0])
    np.testing.assert_allclose(model.pivot_minor_ratios(), [2.0, 1.5])


def test_completed_square_coefficients_reproduce_quadratic_energy():
    model = PositiveDefiniteEliminationTest()
    first, multiplier, second = model.completed_square_coefficients()
    assert (first, multiplier, second) == pytest.approx((2.0, 0.5, 1.5))
    for x1, x2 in ((1.0, 0.0), (0.0, 1.0), (2.0, -3.0), (-0.25, 1.5)):
        completed = first * (x1 + multiplier * x2) ** 2 + second * x2**2
        assert completed == pytest.approx(model.energy([x1, x2]))


def test_positive_tests_agree_for_positive_zero_and_negative_cases():
    cases = (
        ([[2, 1], [1, 2]], True),
        ([[3, 0], [0, 0]], False),
        ([[3, 0], [0, -2]], False),
    )
    for matrix, expected in cases:
        model = PositiveDefiniteEliminationTest(matrix)
        assert model.has_positive_leading_principal_minors() is expected
        assert model.has_positive_elimination_pivots() is expected


def test_higher_dimensional_pivots_are_minor_ratios():
    model = PositiveDefiniteEliminationTest([[4, 2, 0], [2, 3, 1], [0, 1, 2]])
    np.testing.assert_allclose(model.leading_principal_minors(), [4, 8, 12])
    np.testing.assert_allclose(model.elimination_pivots(), [4, 2, 1.5])
    np.testing.assert_allclose(model.pivot_minor_ratios(), [4, 2, 1.5])
    assert model.has_positive_leading_principal_minors()


def test_zero_first_pivot_is_handled_without_claiming_a_positive_test():
    model = PositiveDefiniteEliminationTest([[0, 1], [1, 0]])
    with pytest.raises(ValueError, match="zero pivot"):
        model.elimination_pivots()
    assert not model.has_positive_elimination_pivots()
    assert not model.has_positive_leading_principal_minors()


@pytest.mark.parametrize(
    "bad_matrix",
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [0, 1]], [[1, np.inf], [np.inf, 1]], []),
)
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        PositiveDefiniteEliminationTest(bad_matrix)


def test_rejects_bad_vectors_dimensions_and_tolerances():
    model = PositiveDefiniteEliminationTest()
    with pytest.raises(ValueError):
        model.energy([1, 2, 3])
    with pytest.raises(ValueError):
        model.elimination_pivots(-1.0)
    with pytest.raises(ValueError):
        model.has_positive_leading_principal_minors(float("nan"))
    with pytest.raises(ValueError):
        PositiveDefiniteEliminationTest(np.eye(3)).completed_square_coefficients()
