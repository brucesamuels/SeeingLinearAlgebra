import numpy as np
import pytest
from engine.matrix_composition import MatrixComposition

def test_composition_matches_two_stage_action():
    s = MatrixComposition().snapshot()
    np.testing.assert_allclose(s.after_a_after_b, s.after_ab)

def test_default_products_do_not_commute():
    s = MatrixComposition().snapshot()
    assert not np.array_equal(s.product_ab, s.product_ba)

def test_default_values():
    s = MatrixComposition().snapshot()
    np.testing.assert_allclose(s.after_b, [3.0, 1.0])
    np.testing.assert_allclose(s.after_ab, [-1.0, 3.0])
    np.testing.assert_allclose(s.product_ab, [[0.0, -1.0], [1.0, 1.0]])

@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("matrix_a", np.eye(3)),
        ("matrix_b", np.eye(3)),
        ("vector_x", np.array([1.0, 2.0, 3.0])),
    ],
)
def test_invalid_shapes_raise(name, value):
    with pytest.raises(ValueError):
        MatrixComposition(**{name: value})
