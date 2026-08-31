import numpy as np
import pytest

from engine.minimum_principle import MinimumPrinciple


def test_default_matrix_and_ordered_eigenpairs_are_exact():
    model = MinimumPrinciple()
    expected_vectors = np.array(
        [
            [1 / np.sqrt(2), 1 / np.sqrt(2), 0.0],
            [-1 / np.sqrt(2), 1 / np.sqrt(2), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    values, vectors = model.ordered_eigenpairs()
    assert np.allclose(model.matrix, [[2, 1, 0], [1, 2, 0], [0, 0, 4]])
    assert np.allclose(values, [1, 3, 4])
    assert np.allclose(vectors, expected_vectors)
    assert np.allclose(vectors.T @ vectors, np.eye(3))


@pytest.mark.parametrize(
    ("vector", "expected"),
    [
        ([1, -1, 0], 1.0),
        ([1, 1, 0], 3.0),
        ([0, 0, 2], 4.0),
        ([1, 0, 0], 2.0),
    ],
)
def test_rayleigh_quotient_has_expected_directional_values(vector, expected):
    assert MinimumPrinciple().rayleigh_quotient(vector) == pytest.approx(expected)


def test_rayleigh_quotient_is_scale_invariant():
    first, second = MinimumPrinciple().scale_invariant_pair([2, -1, 3], -7.5)
    assert first == pytest.approx(second)


def test_spectral_formula_matches_direct_rayleigh_quotient():
    model = MinimumPrinciple()
    vector = np.array([2.0, -1.0, 3.0])
    assert model.spectral_rayleigh_quotient(vector) == pytest.approx(
        model.rayleigh_quotient(vector)
    )


def test_eigenvalue_bounds_hold_for_sample_directions():
    model = MinimumPrinciple()
    lower, upper = model.eigenvalue_bounds()
    assert (lower, upper) == pytest.approx((1.0, 4.0))
    for vector in ([1, 0, 0], [2, -3, 4], [-5, 2, 1]):
        quotient = model.rayleigh_quotient(vector)
        assert lower <= quotient <= upper


def test_successive_constraints_recover_each_eigenvalue_and_direction():
    model = MinimumPrinciple()
    values, vectors = model.ordered_eigenpairs()
    for excluded_count in range(3):
        minimum, direction = model.constrained_minimum(excluded_count)
        assert minimum == pytest.approx(values[excluded_count])
        assert np.allclose(direction, vectors[:, excluded_count])
        assert np.allclose(vectors[:, :excluded_count].T @ direction, 0.0)


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        ([], "two-dimensional"),
        ([1.0, 2.0], "two-dimensional"),
        ([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], "square"),
        ([[1.0, 2.0], [0.0, 1.0]], "symmetric"),
        ([[1.0, 0.0], [0.0, 0.0]], "positive definite"),
        ([[1.0, np.inf], [np.inf, 1.0]], "finite"),
    ],
)
def test_invalid_matrices_are_rejected(matrix, message):
    with pytest.raises(ValueError, match=message):
        MinimumPrinciple(matrix)


@pytest.mark.parametrize("vector", ([0, 0, 0], [1, 2], [1, 2, np.inf]))
def test_invalid_vectors_are_rejected(vector):
    with pytest.raises(ValueError):
        MinimumPrinciple().rayleigh_quotient(vector)


@pytest.mark.parametrize("excluded_count", (-1, 3, 1.5))
def test_invalid_constraint_counts_are_rejected(excluded_count):
    with pytest.raises(ValueError, match="excluded_count"):
        MinimumPrinciple().constrained_minimum(excluded_count)


@pytest.mark.parametrize("scale", (0.0, np.inf))
def test_invalid_scales_are_rejected(scale):
    with pytest.raises(ValueError, match="scale"):
        MinimumPrinciple().scale_invariant_pair([1, 0, 0], scale)
