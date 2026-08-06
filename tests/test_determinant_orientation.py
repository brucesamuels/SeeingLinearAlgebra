import numpy as np
import pytest
from engine.determinant_orientation import (
    Orientation, as_matrix_2x2, build_orientation_examples,
    classify_orientation, signed_parallelogram_area, transform_vertices,
)

def test_matrix_validation():
    with pytest.raises(ValueError):
        as_matrix_2x2([[1,2,3],[4,5,6]])

def test_signed_area_positive_and_negative():
    assert signed_parallelogram_area([[2,1],[0,1]]) == pytest.approx(2)
    assert signed_parallelogram_area([[2,1],[0,-1]]) == pytest.approx(-2)

def test_orientation_classification():
    assert classify_orientation(2) is Orientation.PRESERVED
    assert classify_orientation(-2) is Orientation.REVERSED
    assert classify_orientation(0) is Orientation.COLLAPSED

def test_examples_have_equal_area_magnitude_and_opposite_signs():
    positive, negative = build_orientation_examples()
    assert positive.area_scale == negative.area_scale == pytest.approx(2)
    assert positive.signed_scale == pytest.approx(2)
    assert negative.signed_scale == pytest.approx(-2)
    assert positive.orientation is Orientation.PRESERVED
    assert negative.orientation is Orientation.REVERSED

def test_negative_example_is_reflected_below_x_axis():
    _, negative = build_orientation_examples()
    assert np.min(negative.image_vertices[:,1]) == pytest.approx(-1)

def test_transform_vertices_shape():
    assert transform_vertices([[1,0],[0,1]]).shape == (4,2)
