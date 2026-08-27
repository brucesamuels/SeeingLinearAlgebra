import math

import numpy as np
import pytest

from engine.positive_definite_quadratic_surface import QuadraticSurfaceGeometry


def test_default_matrix_and_energy():
    model = QuadraticSurfaceGeometry()
    np.testing.assert_allclose(model.matrix, [[2, 1], [1, 2]])
    assert model.energy([1, 0]) == pytest.approx(2.0)
    assert model.energy([1, 1]) == pytest.approx(6.0)


def test_radial_energy_obeys_quadratic_scaling():
    model = QuadraticSurfaceGeometry()
    theta = math.pi / 7
    base = model.radial_energy(1.0, theta)
    for radius in (0.25, 0.8, 1.7, 3.0):
        assert model.radial_energy(radius, theta) == pytest.approx(radius**2 * base)


def test_surface_point_uses_energy_as_height():
    model = QuadraticSurfaceGeometry()
    point = model.surface_point(0.75, 0.25)
    np.testing.assert_allclose(point[:2], [0.75, 0.25])
    assert point[2] == pytest.approx(model.energy(point[:2]))


def test_surface_origin_is_zero_and_sampled_nonzero_points_are_above_plane():
    model = QuadraticSurfaceGeometry()
    np.testing.assert_allclose(model.surface_point(0, 0), [0, 0, 0])
    for theta in np.linspace(0.0, 2.0 * math.pi, 25, endpoint=False):
        assert model.radial_energy(0.7, theta) > 0.0


def test_surface_height_grid_has_cartesian_shape_and_values():
    model = QuadraticSurfaceGeometry()
    x_values = [-1.0, 0.0, 1.0]
    y_values = [-0.5, 0.5]
    heights = model.surface_heights(x_values, y_values)
    assert heights.shape == (2, 3)
    assert heights[1, 2] == pytest.approx(model.energy([1.0, 0.5]))


@pytest.mark.parametrize(
    "bad_matrix",
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [0, 1]], [[1, np.inf], [np.inf, 1]]),
)
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        QuadraticSurfaceGeometry(bad_matrix)


def test_rejects_invalid_radial_inputs():
    model = QuadraticSurfaceGeometry()
    with pytest.raises(ValueError):
        model.radial_vector(-0.1, 0.0)
    with pytest.raises(ValueError):
        model.radial_vector(1.0, float("nan"))
