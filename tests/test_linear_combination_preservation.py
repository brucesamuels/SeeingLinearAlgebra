import numpy as np
import pytest

from engine.linear_combination_preservation import (
    apply_transformation,
    evaluate_linear_combination_preservation,
)


def test_linear_transformation_preserves_linear_combination():
    snapshot = evaluate_linear_combination_preservation()

    assert snapshot.endpoints_agree
    np.testing.assert_allclose(
        snapshot.transformed_combination,
        snapshot.combination_of_transforms,
        atol=1e-9,
    )


def test_custom_matrix_vectors_and_scalars():
    snapshot = evaluate_linear_combination_preservation(
        matrix=np.array([[2.0, -1.0], [0.5, 1.5]]),
        u=np.array([1.0, 2.0]),
        v=np.array([-2.0, 0.5]),
        a=-1.25,
        b=0.75,
    )

    assert snapshot.endpoints_agree


def test_apply_transformation_validates_shapes():
    with pytest.raises(ValueError):
        apply_transformation(np.eye(3), np.array([1.0, 2.0]))

    with pytest.raises(ValueError):
        apply_transformation(np.eye(2), np.array([1.0, 2.0, 3.0]))
