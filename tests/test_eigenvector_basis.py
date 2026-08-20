import numpy as np
import pytest

from engine.eigenvector_basis import (
    DEFAULT_MATRIX,
    EIGENVALUES,
    EIGENVECTORS,
    EigenvectorBasisLesson,
)


def test_basis_vectors_are_eigenvectors() -> None:
    for i, value in enumerate(EIGENVALUES):
        vector = EIGENVECTORS[:, i]
        assert np.allclose(DEFAULT_MATRIX @ vector, value * vector)


def test_eigenvectors_form_a_basis_for_r3() -> None:
    lesson = EigenvectorBasisLesson()
    assert lesson.basis_is_independent()
    assert np.linalg.matrix_rank(lesson.basis_matrix) == 3


def test_example_has_simple_coordinates() -> None:
    lesson = EigenvectorBasisLesson()
    example = lesson.example()
    assert np.array_equal(example.eigen_coordinates, np.array([1.0, 1.0, 1.0]))
    assert np.array_equal(example.standard_vector, np.array([2.0, -1.0, 1.0]))
    assert np.array_equal(example.transformed_eigen_coordinates, np.array([1.0, 2.0, 5.0]))
    assert np.array_equal(example.transformed_vector, np.array([7.0, 1.0, 1.0]))


def test_coordinate_conversion_round_trips() -> None:
    lesson = EigenvectorBasisLesson()
    vector = np.array([3.0, -4.0, 2.0])
    coordinates = lesson.coordinates_in_eigenbasis(vector)
    assert np.allclose(lesson.reconstruct_from_eigenbasis(coordinates), vector)


def test_bad_vector_shape_is_rejected() -> None:
    lesson = EigenvectorBasisLesson()
    with pytest.raises(ValueError, match="shape"):
        lesson.coordinates_in_eigenbasis([1.0, 2.0])
