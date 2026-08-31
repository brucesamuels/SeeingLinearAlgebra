import numpy as np
import pytest

from engine.covariance_definiteness import CovarianceDefiniteness


def test_default_observations_mean_and_centering_are_exact():
    model = CovarianceDefiniteness()
    assert np.allclose(model.mean(), [3.0, 2.0])
    assert np.allclose(
        model.centered_matrix(),
        [[-2.0, -1.0], [0.0, -1.0], [0.0, 1.0], [2.0, 1.0]],
    )
    assert np.allclose(model.centered_matrix().sum(axis=0), [0.0, 0.0])


def test_population_covariance_has_clean_entries_and_is_positive_definite():
    model = CovarianceDefiniteness()
    assert np.allclose(model.population_covariance(), [[2.0, 1.0], [1.0, 1.0]])
    assert model.covariance_is_positive_semidefinite()
    assert model.covariance_is_positive_definite()


@pytest.mark.parametrize("direction", [[1.0, 0.0], [0.0, 1.0], [2.0, -3.0]])
def test_directional_variance_equals_mean_squared_centered_projection(direction):
    model = CovarianceDefiniteness()
    assert model.directional_variance(direction) == pytest.approx(
        model.squared_projection_mean(direction)
    )


def test_sample_covariance_differs_only_by_positive_scale():
    model = CovarianceDefiniteness()
    assert np.allclose(
        model.sample_covariance(),
        model.population_covariance() * model.observation_count / (model.observation_count - 1),
    )


def test_line_data_have_a_nonzero_zero_variance_direction():
    model = CovarianceDefiniteness([[2.0, 3.0], [3.0, 5.0], [4.0, 7.0]])
    direction = np.array([-2.0, 1.0])
    assert np.allclose(model.mean(), [3.0, 5.0])
    assert np.allclose(model.centered_projections(direction), [0.0, 0.0, 0.0])
    assert model.directional_variance(direction) == pytest.approx(0.0)
    assert model.covariance_is_positive_semidefinite()
    assert not model.covariance_is_positive_definite()


@pytest.mark.parametrize("observations", [[], [[1.0, np.inf]], [1.0, 2.0]])
def test_invalid_observations_are_rejected(observations):
    with pytest.raises(ValueError):
        CovarianceDefiniteness(observations)


def test_invalid_direction_and_sample_size_are_rejected():
    model = CovarianceDefiniteness()
    with pytest.raises(ValueError, match="length"):
        model.directional_variance([1.0])
    with pytest.raises(ValueError, match="finite"):
        model.directional_variance([1.0, np.inf])
    with pytest.raises(ValueError, match="at least two"):
        CovarianceDefiniteness([[1.0, 2.0]]).sample_covariance()
    with pytest.raises(ValueError, match="tolerance"):
        model.covariance_is_positive_semidefinite(-1.0)
