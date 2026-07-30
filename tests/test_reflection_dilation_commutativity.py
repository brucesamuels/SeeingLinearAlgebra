import numpy as np
import pytest

from engine.reflection_dilation_commutativity import (
    dilate,
    evaluate_reflection_dilation,
    reflect,
    reflection_matrix,
)


def test_reflection_matrix_is_involutory():
    angle = np.deg2rad(28.0)
    matrix = reflection_matrix(angle)
    np.testing.assert_allclose(matrix @ matrix, np.eye(2), atol=1e-9)


def test_reflection_and_dilation_commute():
    snapshot = evaluate_reflection_dilation()
    assert snapshot.endpoints_agree
    np.testing.assert_allclose(
        snapshot.reflect_then_dilate,
        snapshot.dilate_then_reflect,
        atol=1e-9,
    )


def test_negative_scalars_are_supported():
    snapshot = evaluate_reflection_dilation(scalar=-1.4)
    assert snapshot.endpoints_agree


def test_vector_dimension_is_validated():
    with pytest.raises(ValueError):
        reflect(np.array([1.0, 2.0, 3.0]), 0.2)
    with pytest.raises(ValueError):
        dilate(np.array([1.0, 2.0, 3.0]), 2.0)
