import numpy as np
import pytest
from engine.basis_determines_transformation import evaluate_basis_determination

def test_reconstruction_matches():
    s=evaluate_basis_determination()
    assert s.agrees
    np.testing.assert_allclose(s.tx,s.rebuilt_tx)

def test_default_vector():
    s=evaluate_basis_determination()
    np.testing.assert_allclose(s.coefficients,[2,1])
    np.testing.assert_allclose(s.x,[2,1])

def test_custom_values():
    s=evaluate_basis_determination(
        matrix=np.array([[2.,-1.],[.5,1.5]]),
        coefficients=np.array([-1.,2.]),
    )
    assert s.agrees

def test_shape_validation():
    with pytest.raises(ValueError):
        evaluate_basis_determination(matrix=np.eye(3))
    with pytest.raises(ValueError):
        evaluate_basis_determination(coefficients=np.array([1.,2.,3.]))
