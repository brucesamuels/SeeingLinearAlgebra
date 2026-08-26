import numpy as np
import pytest

from engine.change_of_basis_review import ChangeOfBasisReview


def test_one_vector_has_expected_three_coordinate_descriptions():
    review = ChangeOfBasisReview()
    np.testing.assert_allclose(review.vector, [3, 1])
    np.testing.assert_allclose(review.coordinates_b(), [2, 1])
    np.testing.assert_allclose(review.coordinates_c(), [1, 1])


def test_transition_columns_and_coordinate_conversion():
    review = ChangeOfBasisReview()
    q = review.transition_c_from_b()
    np.testing.assert_allclose(q, [[1, -1], [0, 1]])
    np.testing.assert_allclose(review.basis_c @ q, review.basis_b)
    np.testing.assert_allclose(review.convert_b_to_c([2, 1]), [1, 1])


def test_reverse_transition_is_inverse():
    review = ChangeOfBasisReview()
    np.testing.assert_allclose(
        review.transition_b_from_c() @ review.transition_c_from_b(),
        np.eye(2),
    )


def test_transformation_becomes_diagonal_in_c_basis():
    review = ChangeOfBasisReview()
    np.testing.assert_allclose(review.transformation_c(), [[2, 0], [0, 3]])
    np.testing.assert_allclose(
        review.basis_c @ review.transformation_c() @ np.linalg.inv(review.basis_c),
        review.standard_transformation(),
    )


def test_rejects_singular_basis():
    with pytest.raises(ValueError):
        ChangeOfBasisReview(basis_b=[[1, 2], [2, 4]])

