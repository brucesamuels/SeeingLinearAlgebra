import numpy as np
import pytest
from engine.standard_to_basis_coordinates import StandardToBasisLesson


def test_default_inverse_and_coordinate_conversion():
    lesson = StandardToBasisLesson()
    np.testing.assert_allclose(lesson.inverse_basis_matrix(), .5 * np.array([[1, 1], [1, -1]]))
    np.testing.assert_allclose(lesson.basis_coordinates(), [3, 1])
    np.testing.assert_allclose(lesson.reconstruct(), [4, 2])


def test_singular_basis_is_rejected():
    with pytest.raises(ValueError, match="invertible"):
        StandardToBasisLesson([[1, 2], [2, 4]], [4, 2])


def test_shape_errors_are_rejected():
    with pytest.raises(ValueError, match="shape"):
        StandardToBasisLesson([[1, 0], [0, 1]], [1, 2, 3])
