import numpy as np
import pytest
from engine.basis_images_to_matrix import evaluate_basis_images_to_matrix

def test_columns_match_matrix():
    s=evaluate_basis_images_to_matrix()
    assert s.columns_match
    np.testing.assert_allclose(s.assembled,s.matrix)

def test_first_column_is_te1():
    s=evaluate_basis_images_to_matrix()
    np.testing.assert_allclose(s.assembled[:,0],s.te1)

def test_second_column_is_te2():
    s=evaluate_basis_images_to_matrix()
    np.testing.assert_allclose(s.assembled[:,1],s.te2)

def test_shape_validation():
    with pytest.raises(ValueError):
        evaluate_basis_images_to_matrix(np.eye(3))
