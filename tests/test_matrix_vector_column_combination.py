import numpy as np
import pytest
from engine.matrix_vector_column_combination import evaluate_matrix_vector_column_combination

def test_product_equals_column_combination():
    s = evaluate_matrix_vector_column_combination()
    assert s.agrees
    np.testing.assert_allclose(s.product, s.reconstructed)

def test_default_contributions():
    s = evaluate_matrix_vector_column_combination()
    np.testing.assert_allclose(s.first_contribution, [2,4])
    np.testing.assert_allclose(s.second_contribution, [-1,1])
    np.testing.assert_allclose(s.product, [1,5])

def test_custom_values():
    s = evaluate_matrix_vector_column_combination(
        matrix=np.array([[2.,3.],[-1.,4.]]),
        vector=np.array([-2.,.5]),
    )
    assert s.agrees

def test_shape_validation():
    with pytest.raises(ValueError):
        evaluate_matrix_vector_column_combination(matrix=np.eye(3))
    with pytest.raises(ValueError):
        evaluate_matrix_vector_column_combination(vector=np.array([1.,2.,3.]))
