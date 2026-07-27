import numpy as np
import pytest

from engine.basis_dimension import BasisDimension

V1 = np.array([2.0, 0.2, 0.4])
V2 = np.array([-0.4, 1.7, 0.9])
V3 = V1 + V2
PAIRS = np.array([(a, b) for a in (-1.0, 0.0, 1.0) for b in (-1.0, 0.0, 1.0)], dtype=float)
TRIPLES = np.array([(a, b, c) for a in (-1.0, 0.0, 1.0) for b in (-1.0, 0.0, 1.0) for c in (-1.0, 0.0, 1.0)], dtype=float)


def _model() -> BasisDimension:
    return BasisDimension(V1, V2, V3, PAIRS, TRIPLES)


def test_snapshot_reports_rank_two_and_dimension_two() -> None:
    snapshot = _model().snapshot()
    assert snapshot.rank == 2
    assert snapshot.dimension == 2


def test_vector_three_is_expressed_in_terms_of_basis() -> None:
    coefficients = _model().express_vector_3_in_basis()
    assert np.allclose(coefficients, np.array([1.0, 1.0]), atol=1e-9)


def test_spans_match_after_removing_redundant_vector() -> None:
    assert _model().spans_match()


def test_basis_vectors_are_independent() -> None:
    matrix = np.column_stack(_model().basis_vectors)
    assert np.linalg.matrix_rank(matrix) == 2


def test_endpoints_from_pairs_have_shape_n_by_three() -> None:
    endpoints = _model().endpoints_from_pairs(PAIRS)
    assert endpoints.shape == (len(PAIRS), 3)


def test_endpoints_from_triples_have_shape_n_by_three() -> None:
    endpoints = _model().endpoints_from_triples(TRIPLES)
    assert endpoints.shape == (len(TRIPLES), 3)


def test_invalid_pair_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        BasisDimension(V1, V2, V3, np.zeros((3, 3)), TRIPLES)


def test_invalid_triple_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        BasisDimension(V1, V2, V3, PAIRS, np.zeros((3, 2)))


def test_nonredundant_third_vector_is_rejected() -> None:
    with pytest.raises(ValueError):
        BasisDimension(V1, V2, np.array([0.0, 0.0, 1.0]), PAIRS, TRIPLES)
