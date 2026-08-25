import numpy as np
import pytest

from engine.transformation_between_bases import TransformationBetweenBasesLesson


def test_direct_transition_and_similarity_formula():
    lesson = TransformationBetweenBasesLesson()
    np.testing.assert_allclose(lesson.transition_c_from_b(), [[1, -1], [0, 1]])
    np.testing.assert_allclose(lesson.basis_b_coordinates_in_c(), [[1, -1], [0, 1]])
    np.testing.assert_allclose(lesson.transition_b_from_c(), [[1, 1], [0, 1]])
    np.testing.assert_allclose(lesson.matrix_c(), [[2, 0], [0, 3]])
    basis_c = np.array([[1.0, 2.0], [1.0, 0.0]])
    basis_b = np.array([[1.0, 1.0], [1.0, -1.0]])
    np.testing.assert_allclose(basis_c @ lesson.basis_b_coordinates_in_c(), basis_b)


def test_augmented_reduction_computes_old_to_new_transition():
    lesson = TransformationBetweenBasesLesson()
    states = lesson.transition_reduction_states()
    expected = (
        [[1, 2, 1, 1], [1, 0, 1, -1]],
        [[1, 2, 1, 1], [0, -2, 0, -2]],
        [[1, 2, 1, 1], [0, 1, 0, 1]],
        [[1, 0, 1, -1], [0, 1, 0, 1]],
    )
    assert len(states) == len(expected)
    for actual, target in zip(states, expected):
        np.testing.assert_allclose(actual, target)
    np.testing.assert_allclose(states[-1][:, :2], np.eye(2))
    np.testing.assert_allclose(states[-1][:, 2:], lesson.transition_c_from_b())


def test_same_input_and_output_in_both_coordinate_languages():
    lesson = TransformationBetweenBasesLesson()
    input_b = np.array([2.0, 1.0])
    output_b = lesson.transform_in_b(input_b)
    input_c = lesson.coordinates_c(input_b)
    output_c = lesson.coordinates_c(output_b)
    np.testing.assert_allclose(output_b, [5, 3])
    np.testing.assert_allclose(input_c, [1, 1])
    np.testing.assert_allclose(output_c, [2, 3])
    np.testing.assert_allclose(lesson.transform_in_c(input_c), output_c)


def test_singular_bases_are_rejected():
    with pytest.raises(ValueError, match="basis B"):
        TransformationBetweenBasesLesson(basis_b=[[1, 2], [2, 4]])
    with pytest.raises(ValueError, match="basis C"):
        TransformationBetweenBasesLesson(basis_c=[[1, 2], [2, 4]])
