import numpy as np
import pytest
from engine.transformation_matrix_basis import TransformationMatrixBasisLesson


def test_default_similarity_and_vector_check():
    lesson = TransformationMatrixBasisLesson()
    np.testing.assert_allclose(lesson.matrix_in_basis(), [[2, 1], [0, 1]])
    np.testing.assert_allclose(lesson.input_standard(), [3, 2])
    np.testing.assert_allclose(lesson.output_standard(), [6, 2])
    np.testing.assert_allclose(lesson.output_basis(), [4, 2])


def test_singular_basis_is_rejected():
    with pytest.raises(ValueError, match="invertible"):
        TransformationMatrixBasisLesson(basis_matrix=[[1, 2], [2, 4]])
