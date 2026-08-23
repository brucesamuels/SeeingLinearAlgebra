import numpy as np
import pytest
from engine.two_basis_coordinates import TwoBasisCoordinatesLesson


def test_default_transition_and_coordinates():
    lesson = TwoBasisCoordinatesLesson()
    np.testing.assert_allclose(lesson.transition_b_to_c(), [[1, -1], [0, 1]])
    np.testing.assert_allclose(lesson.standard_vector(), [4, 2])
    np.testing.assert_allclose(lesson.coordinates_c(), [2, 1])


def test_singular_basis_is_rejected():
    with pytest.raises(ValueError, match="invertible"):
        TwoBasisCoordinatesLesson(basis_c=[[1, 2], [2, 4]])
