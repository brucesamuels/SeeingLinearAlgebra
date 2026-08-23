import numpy as np
import pytest

from engine.basis_matrix import BasisMatrixLesson


def test_basis_vectors_are_columns_of_basis_matrix() -> None:
    lesson = BasisMatrixLesson()
    assert np.allclose(lesson.basis_vector(0), [1.0, 1.0])
    assert np.allclose(lesson.basis_vector(1), [1.0, -1.0])


def test_basis_matrix_synthesizes_standard_vector() -> None:
    lesson = BasisMatrixLesson()
    assert np.allclose(lesson.synthesize(), [4.0, 2.0])
    assert np.allclose(lesson.basis_matrix @ lesson.basis_coordinates, [4.0, 2.0])


def test_standard_basis_coordinate_inputs_return_basis_columns() -> None:
    lesson = BasisMatrixLesson()
    assert np.allclose(lesson.synthesize([1.0, 0.0]), lesson.basis_vector(0))
    assert np.allclose(lesson.synthesize([0.0, 1.0]), lesson.basis_vector(1))


def test_detailed_worked_example_converts_to_standard_coordinates() -> None:
    lesson = BasisMatrixLesson()
    assert np.allclose(lesson.worked_standard_coordinates(), [1.0, 3.0])
    example = lesson.example()
    assert np.allclose(example.worked_coordinates, [2.0, -1.0])
    assert np.allclose(example.worked_standard_coordinates, [1.0, 3.0])


def test_singular_basis_matrix_is_rejected() -> None:
    with pytest.raises(ValueError, match="invertible"):
        BasisMatrixLesson(basis_matrix=np.array([[1.0, 2.0], [2.0, 4.0]]))
