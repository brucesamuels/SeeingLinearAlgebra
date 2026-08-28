import math

import numpy as np
import pytest

from engine.positive_definite_eigenvalue_test import PositiveDefiniteEigenvalueTest


def test_default_eigenvalues_and_orthonormal_eigenvectors():
    model = PositiveDefiniteEigenvalueTest()
    np.testing.assert_allclose(model.eigenvalues(), [1, 3])
    vectors = model.eigenvectors()
    np.testing.assert_allclose(vectors.T @ vectors, np.eye(2), atol=1e-12)
    np.testing.assert_allclose(
        model.matrix @ vectors,
        vectors @ np.diag(model.eigenvalues()),
        atol=1e-12,
    )


def test_special_unit_directions_have_extreme_energies():
    model = PositiveDefiniteEigenvalueTest()
    assert model.directional_energy(math.pi / 4) == pytest.approx(3.0)
    assert model.directional_energy(-math.pi / 4) == pytest.approx(1.0)
    assert model.unit_energy_bounds() == pytest.approx((1.0, 3.0))


def test_spectral_energy_equals_direct_quadratic_energy():
    model = PositiveDefiniteEigenvalueTest()
    for vector in ([2.0, -1.0], [0.25, 0.75], [-3.0, 4.0]):
        assert model.spectral_energy(vector) == pytest.approx(model.energy(vector))
        assert sum(model.spectral_energy_terms(vector)) == pytest.approx(
            model.energy(vector)
        )


def test_positive_definite_classification_uses_eigenvalue_signs():
    assert PositiveDefiniteEigenvalueTest([[2, 1], [1, 2]]).is_positive_definite()
    assert not PositiveDefiniteEigenvalueTest([[3, 0], [0, 0]]).is_positive_definite()
    assert not PositiveDefiniteEigenvalueTest([[3, 0], [0, -3]]).is_positive_definite()


def test_supports_higher_dimensional_symmetric_matrices():
    model = PositiveDefiniteEigenvalueTest(np.diag([0.5, 2.0, 4.0]))
    np.testing.assert_allclose(model.eigenvalues(), [0.5, 2.0, 4.0])
    assert model.is_positive_definite()
    assert model.spectral_energy([1, 2, 3]) == pytest.approx(
        model.energy([1, 2, 3])
    )


@pytest.mark.parametrize(
    "bad_matrix",
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [0, 1]], [[1, np.inf], [np.inf, 1]], []),
)
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        PositiveDefiniteEigenvalueTest(bad_matrix)


def test_rejects_bad_vectors_angles_and_tolerances():
    model = PositiveDefiniteEigenvalueTest()
    with pytest.raises(ValueError):
        model.energy([1, 2, 3])
    with pytest.raises(ValueError):
        model.direction(float("nan"))
    with pytest.raises(ValueError):
        model.is_positive_definite(-1.0)
    with pytest.raises(ValueError):
        PositiveDefiniteEigenvalueTest(np.eye(3)).directional_energy(0.0)
