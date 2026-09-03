import inspect

import numpy as np
import pytest

from engine.truncated_svd_approximation import TruncatedSVDApproximation


def test_default_matrix_and_singular_values_are_exact():
    model = TruncatedSVDApproximation()
    assert np.allclose(model.matrix, np.diag([5, 2, 0.5]))
    assert np.allclose(model.singular_values(), [5, 2, 0.5])
    assert model.maximum_rank == 3


def test_rank_one_layers_reconstruct_the_matrix():
    model = TruncatedSVDApproximation()
    components = model.rank_one_components()
    assert len(components) == 3
    assert all(np.linalg.matrix_rank(component) == 1 for component in components)
    assert np.allclose(model.reconstruct(), model.matrix)


@pytest.mark.parametrize(
    "rank, expected",
    (
        (0, np.zeros((3, 3))),
        (1, np.diag([5, 0, 0])),
        (2, np.diag([5, 2, 0])),
        (3, np.diag([5, 2, 0.5])),
    ),
)
def test_truncation_keeps_largest_rank_one_layers(rank, expected):
    assert np.allclose(TruncatedSVDApproximation().truncated(rank), expected)


@pytest.mark.parametrize(
    "rank, spectral, frobenius",
    ((0, 5, np.sqrt(29.25)), (1, 2, np.sqrt(4.25)), (2, 0.5, 0.5), (3, 0, 0)),
)
def test_truncation_errors_match_discarded_singular_values(rank, spectral, frobenius):
    model = TruncatedSVDApproximation()
    assert model.spectral_error(rank) == pytest.approx(spectral)
    assert model.frobenius_error(rank) == pytest.approx(frobenius)
    assert model.optimal_spectral_error(rank) == pytest.approx(spectral)
    assert model.optimal_frobenius_error(rank) == pytest.approx(frobenius)


def test_keeping_largest_two_layers_beats_discarding_middle_layer():
    model = TruncatedSVDApproximation()
    best = model.selected_spectral_error([0, 1])
    alternative = model.selected_spectral_error([0, 2])
    assert best == pytest.approx(0.5)
    assert alternative == pytest.approx(2)
    assert best < alternative


def test_rectangular_matrix_is_supported():
    matrix = np.array([[3, 0], [0, 1], [0, 0]], dtype=float)
    model = TruncatedSVDApproximation(matrix)
    assert model.maximum_rank == 2
    assert np.allclose(model.reconstruct(), matrix)
    assert model.spectral_error(1) == pytest.approx(1)


@pytest.mark.parametrize("matrix", ([], [1, 2], [[1, np.inf]], [[np.nan]]))
def test_invalid_matrices_are_rejected(matrix):
    with pytest.raises(ValueError, match="matrix"):
        TruncatedSVDApproximation(matrix)


@pytest.mark.parametrize("rank", (-1, 4, 1.5, True))
def test_invalid_truncation_ranks_are_rejected(rank):
    with pytest.raises(ValueError, match="rank"):
        TruncatedSVDApproximation().truncated(rank)


@pytest.mark.parametrize("indices, message", (([0, 0], "unique"), ([3], "range"), ([-1], "range"), ([1.5], "integers"), ([True], "integers")))
def test_invalid_component_selections_are_rejected(indices, message):
    with pytest.raises(ValueError, match=message):
        TruncatedSVDApproximation().selected_components(indices)


def test_engine_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(TruncatedSVDApproximation))
    assert "from manim" not in source
    assert "import manim" not in source
