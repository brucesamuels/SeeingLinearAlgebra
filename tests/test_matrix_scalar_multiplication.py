import pytest
from engine.matrix_scalar_multiplication import *
def test_scale(): assert scale_matrix(3,((2,-1),(0,4)))==((6,-3),(0,12))
def test_shape():
 m=((1,2,3),(4,5,6)); assert matrix_shape(scale_matrix(-2,m))==matrix_shape(m)
def test_zero(): assert scale_matrix(0,((1,-2),(3,4)))==((0,0),(0,0))
def test_negative(): assert scale_matrix(-2,((2,-1),(0,4)))==((-4,2),(0,-8))
def test_steps(): assert [s.result for s in scalar_entry_steps(3,((2,-1),(0,4)))]==[6,-3,0,12]
def test_distributive():
 L=MATRIX_SCALAR_MULTIPLICATION_LESSON; assert L.distributive_left==L.distributive_right
def test_invalid():
 with pytest.raises(ValueError): scale_matrix(2,())
 with pytest.raises(ValueError): scale_matrix(2,((1,2),(3,)))
