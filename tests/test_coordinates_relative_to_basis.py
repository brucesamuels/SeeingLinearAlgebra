import numpy as np
import pytest

from engine.coordinates_relative_to_basis import CoordinatesRelativeToBasisLesson


def test_default_coordinates_are_three_and_one() -> None:
    lesson = CoordinatesRelativeToBasisLesson()
    assert np.allclose(lesson.coordinates(), [3.0, 1.0])


def test_coordinates_reconstruct_geometric_vector() -> None:
    lesson = CoordinatesRelativeToBasisLesson()
    assert np.allclose(lesson.reconstruct(), [4.0, 2.0])
    assert np.allclose(lesson.reconstruct(), lesson.vector)


def test_combination_path_ends_at_fixed_vector() -> None:
    lesson = CoordinatesRelativeToBasisLesson()
    points = lesson.combination_points()
    assert points.shape == (5, 2)
    assert np.allclose(points[-1], lesson.vector)
    assert np.allclose(points[3], [3.0, 3.0])


def test_reversing_basis_reverses_coordinate_order() -> None:
    lesson = CoordinatesRelativeToBasisLesson()
    assert np.allclose(lesson.reversed_coordinates(), [1.0, 3.0])
    assert np.allclose(lesson.reversed_basis() @ lesson.reversed_coordinates(), lesson.vector)


def test_dependent_basis_is_rejected() -> None:
    with pytest.raises(ValueError, match="linearly independent"):
        CoordinatesRelativeToBasisLesson(basis=np.array([[1.0, 2.0], [2.0, 4.0]]))

