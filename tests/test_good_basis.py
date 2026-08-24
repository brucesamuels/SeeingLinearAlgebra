import numpy as np
import pytest
from engine.good_basis import GoodBasisLesson


def test_good_basis_diagonalizes_the_example():
    lesson = GoodBasisLesson()
    np.testing.assert_allclose(lesson.matrix_in_basis(), [[4, 0], [0, 2]])
    np.testing.assert_allclose(lesson.basis_image(0), [4, 4])
    np.testing.assert_allclose(lesson.basis_image(1), [2, -2])
    np.testing.assert_allclose(lesson.convert_basis_vector([2, 1]), [8, 2])


def test_singular_basis_is_rejected():
    with pytest.raises(ValueError, match="invertible"):
        GoodBasisLesson(basis_matrix=[[1, 2], [2, 4]])
