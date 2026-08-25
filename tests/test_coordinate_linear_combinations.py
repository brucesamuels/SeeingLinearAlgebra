import numpy as np
import pytest

from engine.coordinate_linear_combinations import CoordinateLinearCombinationsLesson


def test_default_vector_has_two_correct_recipes():
    lesson = CoordinateLinearCombinationsLesson()
    np.testing.assert_allclose(lesson.standard_coordinates(), [3, 2])
    np.testing.assert_allclose(lesson.basis_coordinates(), [1, 2])
    np.testing.assert_allclose(lesson.reconstruct_from_basis([1, 2]), [3, 2])


def test_columns_are_basis_vectors_in_standard_coordinates():
    lesson = CoordinateLinearCombinationsLesson()
    np.testing.assert_allclose(lesson.basis_vectors_in_standard_coordinates(), [[1, 1], [0, 1]])


def test_transition_columns_are_source_vectors_in_target_coordinates():
    source = np.array([[1, 1], [0, 1]], dtype=float)
    target = np.array([[1, 2], [1, 0]], dtype=float)
    transition = CoordinateLinearCombinationsLesson.transition_matrix(target, source)
    np.testing.assert_allclose(target @ transition, source)


def test_rejects_singular_basis():
    with pytest.raises(ValueError):
        CoordinateLinearCombinationsLesson([[1, 2], [2, 4]])

