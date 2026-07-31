import numpy as np
import pytest

from engine.cross_product_computation import CrossProductComputation


def test_default_example_computes_expected_result():
    s = CrossProductComputation().snapshot()

    np.testing.assert_allclose(s.result, [-10.0, -1.0, 7.0])
    assert s.i_coefficient == pytest.approx(-10.0)
    assert s.j_coefficient == pytest.approx(-1.0)
    assert s.k_coefficient == pytest.approx(7.0)


def test_default_minors_are_correct():
    s = CrossProductComputation().snapshot()

    np.testing.assert_allclose(s.i_minor, [[1.0, 3.0], [4.0, 2.0]])
    np.testing.assert_allclose(s.j_minor, [[2.0, 3.0], [1.0, 2.0]])
    np.testing.assert_allclose(s.k_minor, [[2.0, 1.0], [1.0, 4.0]])


def test_middle_component_uses_negative_cofactor_sign():
    s = CrossProductComputation().snapshot()

    assert s.j_determinant == pytest.approx(1.0)
    assert s.j_coefficient == pytest.approx(-1.0)


def test_result_is_perpendicular_to_both_inputs():
    s = CrossProductComputation().snapshot()

    assert s.dot_u_result == pytest.approx(0.0)
    assert s.dot_v_result == pytest.approx(0.0)


def test_result_matches_numpy_cross_product():
    s = CrossProductComputation([3, -2, 5], [4, 1, -1]).snapshot()

    np.testing.assert_allclose(
        s.result,
        np.cross([3, -2, 5], [4, 1, -1]),
    )


@pytest.mark.parametrize(
    "matrix",
    [
        [1, 2, 3],
        [[1, 2, 3], [4, 5, 6]],
        [[1], [2]],
    ],
)
def test_determinant_2x2_rejects_wrong_shape(matrix):
    with pytest.raises(ValueError):
        CrossProductComputation.determinant_2x2(matrix)


@pytest.mark.parametrize(
    ("vector_u", "vector_v"),
    [
        ([1, 2], [3, 4, 5]),
        ([1, 2, 3], [4, 5, 6, 7]),
    ],
)
def test_invalid_vector_dimensions_raise(vector_u, vector_v):
    with pytest.raises(ValueError):
        CrossProductComputation(vector_u, vector_v)
