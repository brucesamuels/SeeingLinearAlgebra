import math
import numpy as np
import pytest
from engine.inner_product import InnerProduct

def test_default_dot_product_and_geometry():
    s = InnerProduct().snapshot()
    assert s.value == pytest.approx(6.0)
    assert s.norm_u == pytest.approx(3.0)
    assert s.norm_v == pytest.approx(math.sqrt(8.0))
    assert s.cosine == pytest.approx(1 / math.sqrt(2))
    assert s.angle_degrees == pytest.approx(45.0)
    assert s.classification == 'acute'

@pytest.mark.parametrize(('vector_v','expected_value','expected_classification'), [([0.0,2.0],0.0,'right'),([-2.0,2.0],-6.0,'obtuse'),([2.0,2.0],6.0,'acute')])
def test_sign_classifies_angle(vector_v, expected_value, expected_classification):
    s = InnerProduct([3.0,0.0], vector_v).snapshot()
    assert s.value == pytest.approx(expected_value)
    assert s.classification == expected_classification

def test_projection_onto_first_vector():
    s = InnerProduct([3.0,0.0],[2.0,2.0]).snapshot()
    assert s.projection_scalar == pytest.approx(2/3)
    np.testing.assert_allclose(s.projection_vector,[2.0,0.0])

def test_dot_supports_higher_dimensions():
    assert InnerProduct.dot([1,2,3],[4,5,6]) == pytest.approx(32.0)

@pytest.mark.parametrize(('vector_u','vector_v'), [([1.0,2.0],[1.0,2.0,3.0]), ([[1.0,2.0]],[[3.0,4.0]])])
def test_invalid_vector_dimensions_raise(vector_u, vector_v):
    with pytest.raises(ValueError): InnerProduct(vector_u, vector_v)

@pytest.mark.parametrize(('vector_u','vector_v'), [([0.0,0.0],[1.0,0.0]),([1.0,0.0],[0.0,0.0])])
def test_zero_vector_angle_raises(vector_u, vector_v):
    with pytest.raises(ValueError): InnerProduct(vector_u, vector_v).snapshot()

def test_nonpositive_tolerance_raises():
    with pytest.raises(ValueError): InnerProduct(zero_tolerance=0.0)
