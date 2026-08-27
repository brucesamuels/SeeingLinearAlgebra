import math

import numpy as np
import pytest

from engine.positive_definite_directional_energy import DirectionalQuadraticEnergy


def test_default_matrix_and_unit_directions():
    model = DirectionalQuadraticEnergy()
    np.testing.assert_allclose(model.matrix, [[2, 1], [1, 2]])
    for theta in (0.0, math.pi / 3, math.pi, 1.7 * math.pi):
        assert np.linalg.norm(model.direction(theta)) == pytest.approx(1.0)


def test_energy_matches_direct_matrix_product():
    model = DirectionalQuadraticEnergy()
    vector = np.array([0.6, 0.8])
    assert model.energy(vector) == pytest.approx(float(vector @ model.matrix @ vector))


def test_sampled_nonzero_directions_have_positive_energy():
    model = DirectionalQuadraticEnergy()
    angles = np.linspace(0.0, 2.0 * math.pi, 37)
    samples = model.directional_samples(angles)
    assert len(samples) == len(angles)
    assert all(value > 0.0 for _, value in samples)


def test_energy_scales_quadratically():
    model = DirectionalQuadraticEnergy()
    vector = np.array([2.0, -1.0])
    assert model.energy(3.0 * vector) == pytest.approx(9.0 * model.energy(vector))


@pytest.mark.parametrize(
    "bad_matrix",
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [0, 1]], [[1, np.inf], [np.inf, 1]]),
)
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        DirectionalQuadraticEnergy(bad_matrix)


def test_rejects_invalid_vectors_and_angles():
    model = DirectionalQuadraticEnergy()
    with pytest.raises(ValueError):
        model.energy([1, 2, 3])
    with pytest.raises(ValueError):
        model.direction(float("nan"))
