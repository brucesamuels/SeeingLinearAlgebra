import numpy as np
import pytest

from engine.positive_definite_ldlt import PositiveDefiniteLDLT


def test_default_factorization_records_expected_multipliers_and_pivots():
    model = PositiveDefiniteLDLT()
    np.testing.assert_allclose(
        model.lower_factor(),
        [[1, 0, 0], [0.5, 1, 0], [0, 0.5, 1]],
    )
    np.testing.assert_allclose(model.diagonal_entries(), [4, 2, 1.5])


def test_factorization_reconstructs_default_matrix():
    model = PositiveDefiniteLDLT()
    np.testing.assert_allclose(model.reconstruct(), model.matrix, atol=1e-12)


def test_transformed_coordinates_give_completed_square_variables():
    model = PositiveDefiniteLDLT()
    np.testing.assert_allclose(
        model.transformed_coordinates([2, -1, 4]),
        [1.5, 1.0, 4.0],
    )


def test_diagonal_energy_equals_direct_quadratic_energy():
    model = PositiveDefiniteLDLT()
    for vector in ([1, 0, 0], [2, -1, 4], [-0.5, 1.25, 3]):
        assert model.diagonal_energy(vector) == pytest.approx(model.energy(vector))
        assert sum(model.diagonal_energy_terms(vector)) == pytest.approx(
            model.energy(vector)
        )


def test_positive_diagonal_distinguishes_sign_cases():
    assert PositiveDefiniteLDLT(np.diag([3, 2, 1])).has_positive_diagonal()
    assert not PositiveDefiniteLDLT(np.diag([3, 2, 0])).has_positive_diagonal()
    assert not PositiveDefiniteLDLT(np.diag([3, 2, -1])).has_positive_diagonal()


def test_supports_general_symmetric_dimension():
    model = PositiveDefiniteLDLT([[2, 1], [1, 2]])
    np.testing.assert_allclose(model.diagonal_entries(), [2, 1.5])
    np.testing.assert_allclose(model.reconstruct(), [[2, 1], [1, 2]])


@pytest.mark.parametrize(
    "bad_matrix",
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [0, 1]], [[1, np.inf], [np.inf, 1]], []),
)
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        PositiveDefiniteLDLT(bad_matrix)


def test_rejects_zero_intermediate_pivot_and_bad_inputs():
    with pytest.raises(ValueError, match="zero pivot"):
        PositiveDefiniteLDLT([[0, 1], [1, 0]])
    with pytest.raises(ValueError):
        PositiveDefiniteLDLT(tolerance=-1)
    model = PositiveDefiniteLDLT()
    with pytest.raises(ValueError):
        model.energy([1, 2])
    with pytest.raises(ValueError):
        model.has_positive_diagonal(float("nan"))
