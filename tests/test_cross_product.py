import numpy as np
import pytest

from engine.cross_product import CrossProduct


def test_default_cross_product():
    s = CrossProduct().snapshot()

    np.testing.assert_allclose(s.cross_uv, [0.0, 0.0, 6.0])
    np.testing.assert_allclose(s.cross_vu, [0.0, 0.0, -6.0])
    assert s.magnitude == pytest.approx(6.0)
    assert s.parallelogram_area == pytest.approx(6.0)
    assert not s.is_degenerate


def test_cross_product_is_perpendicular_to_both_inputs():
    s = CrossProduct().snapshot()

    assert s.dot_u_cross == pytest.approx(0.0)
    assert s.dot_v_cross == pytest.approx(0.0)


def test_reversing_order_negates_result():
    s = CrossProduct([1, 2, 3], [4, 5, 6]).snapshot()

    np.testing.assert_allclose(s.cross_vu, -s.cross_uv)


def test_parallel_vectors_have_zero_cross_product():
    s = CrossProduct([1, 2, 3], [2, 4, 6]).snapshot()

    np.testing.assert_allclose(s.cross_uv, [0.0, 0.0, 0.0])
    assert s.is_degenerate
    assert s.parallelogram_area == pytest.approx(0.0)


@pytest.mark.parametrize(
    ("vector_u", "vector_v"),
    [
        ([1, 2], [3, 4, 5]),
        ([1, 2, 3, 4], [1, 2, 3]),
    ],
)
def test_invalid_dimensions_raise(vector_u, vector_v):
    with pytest.raises(ValueError):
        CrossProduct(vector_u, vector_v)


@pytest.mark.parametrize(
    ("vector_u", "vector_v"),
    [
        ([0, 0, 0], [1, 0, 0]),
        ([1, 0, 0], [0, 0, 0]),
    ],
)
def test_zero_vectors_raise_when_snapshot_requested(vector_u, vector_v):
    with pytest.raises(ValueError):
        CrossProduct(vector_u, vector_v).snapshot()


def test_static_cross_method():
    np.testing.assert_allclose(
        CrossProduct.cross([1, 0, 0], [0, 1, 0]),
        [0, 0, 1],
    )
