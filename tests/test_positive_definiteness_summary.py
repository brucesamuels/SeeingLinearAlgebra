import numpy as np
import pytest

from engine.positive_definiteness_summary import PositiveDefinitenessSummary


def test_default_matrix_has_expected_eigenvalues_energy_and_classification():
    model = PositiveDefinitenessSummary()
    assert np.allclose(model.matrix, [[2, 1], [1, 2]])
    assert np.allclose(model.eigenvalues(), [1, 3])
    assert model.inertia() == (2, 0, 0)
    assert model.classification() == "positive definite"
    assert model.energy([1, -1]) == pytest.approx(2)


def test_default_matrix_has_positive_minors_and_pivots():
    model = PositiveDefinitenessSummary()
    assert np.allclose(model.leading_principal_minors(), [2, 3])
    assert np.allclose(model.elimination_pivots(), [2, 3 / 2])


def test_default_ldl_and_cholesky_factorizations_reconstruct_matrix():
    model = PositiveDefinitenessSummary()
    lower, diagonal = model.ldl_factorization()
    upper = model.cholesky_upper()
    assert np.allclose(lower, [[1, 0], [1 / 2, 1]])
    assert np.allclose(diagonal, [[2, 0], [0, 3 / 2]])
    assert np.allclose(lower @ diagonal @ lower.T, model.matrix)
    assert np.allclose(upper.T @ upper, model.matrix)


def test_all_default_positive_definite_checks_agree():
    assert PositiveDefinitenessSummary().positive_definite_checks() == {
        "eigenvalues": True,
        "leading_principal_minors": True,
        "elimination_pivots": True,
        "cholesky": True,
    }


@pytest.mark.parametrize(
    ("matrix", "classification", "inertia"),
    [
        ([[1, 1], [1, 1]], "positive semidefinite", (1, 0, 1)),
        ([[1, 0], [0, -1]], "indefinite", (1, 1, 0)),
        ([[-2, 0], [0, -1]], "negative definite", (0, 2, 0)),
        ([[-1, 0], [0, 0]], "negative semidefinite", (0, 1, 1)),
        ([[0, 0], [0, 0]], "zero", (0, 0, 2)),
    ],
)
def test_symmetric_matrix_classifications(matrix, classification, inertia):
    model = PositiveDefinitenessSummary(matrix)
    assert model.classification() == classification
    assert model.inertia() == inertia


def test_semidefinite_and_indefinite_example_energies_expose_the_difference():
    semidefinite = PositiveDefinitenessSummary([[1, 1], [1, 1]])
    indefinite = PositiveDefinitenessSummary([[1, 0], [0, -1]])
    assert semidefinite.energy([1, -1]) == pytest.approx(0)
    assert semidefinite.energy([1, 1]) > 0
    assert indefinite.energy([1, 0]) > 0
    assert indefinite.energy([0, 1]) < 0


@pytest.mark.parametrize(
    "matrix",
    (
        [[1, 1], [1, 1]],
        [[1, 0], [0, -1]],
    ),
)
def test_non_positive_definite_examples_fail_all_equivalent_checks(matrix):
    assert not any(PositiveDefinitenessSummary(matrix).positive_definite_checks().values())


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        ([], "two-dimensional"),
        ([1, 2], "two-dimensional"),
        ([[1, 0, 0], [0, 1, 0]], "square"),
        ([[1, 2], [0, 1]], "symmetric"),
        ([[1, np.inf], [np.inf, 1]], "finite"),
    ],
)
def test_invalid_matrices_are_rejected(matrix, message):
    with pytest.raises(ValueError, match=message):
        PositiveDefinitenessSummary(matrix)


@pytest.mark.parametrize("tolerance", (0, -1, np.inf))
def test_invalid_tolerances_are_rejected(tolerance):
    with pytest.raises(ValueError, match="tolerance"):
        PositiveDefinitenessSummary(tolerance=tolerance)


@pytest.mark.parametrize("vector", ([1], [1, np.inf]))
def test_invalid_energy_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="vector"):
        PositiveDefinitenessSummary().energy(vector)
