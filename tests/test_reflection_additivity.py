import numpy as np
import pytest

from engine.reflection_additivity import (
    evaluate_reflection_additivity,
    reflect,
    reflection_matrix,
)


def test_reflection_preserves_addition():
    snapshot = evaluate_reflection_additivity()

    assert snapshot.endpoints_agree
    np.testing.assert_allclose(
        snapshot.reflected_sum,
        snapshot.sum_of_reflections,
        atol=1e-9,
    )


def test_default_vectors_have_wide_angular_separation():
    snapshot = evaluate_reflection_additivity()
    cosine = np.dot(snapshot.u, snapshot.v) / (
        np.linalg.norm(snapshot.u) * np.linalg.norm(snapshot.v)
    )

    # Negative cosine means the angle is greater than 90 degrees.
    assert cosine < 0


def test_reflection_matrix_is_linear():
    angle = np.deg2rad(24.0)
    matrix = reflection_matrix(angle)
    u = np.array([1.2, -0.4])
    v = np.array([-0.5, 1.7])

    np.testing.assert_allclose(
        matrix @ (u + v),
        matrix @ u + matrix @ v,
        atol=1e-9,
    )


def test_custom_vectors_are_supported():
    snapshot = evaluate_reflection_additivity(
        u=np.array([2.0, 1.0]),
        v=np.array([-1.0, 0.5]),
    )
    assert snapshot.endpoints_agree


def test_dimension_validation():
    with pytest.raises(ValueError):
        reflect(np.array([1.0, 2.0, 3.0]), 0.2)
