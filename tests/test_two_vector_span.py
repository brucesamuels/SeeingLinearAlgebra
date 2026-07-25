import numpy as np
import pytest

from engine.two_vector_span import TwoVectorSpan


def test_snapshot_computes_terms_and_endpoint_exactly() -> None:
    model = TwoVectorSpan((2.0, 1.0), (-1.0, 3.0))
    snapshot = model.snapshot(1.5, -2.0)

    np.testing.assert_allclose(snapshot.term_u, (3.0, 1.5))
    np.testing.assert_allclose(snapshot.term_v, (2.0, -6.0))
    np.testing.assert_allclose(snapshot.endpoint, (5.0, -4.5))
    assert snapshot.dimension == 2


def test_fixed_u_coefficient_produces_a_line_parallel_to_v() -> None:
    model = TwoVectorSpan((2.0, 0.0), (0.0, 3.0))
    line = model.fixed_u_line(1.5, -2.0, 2.0)

    np.testing.assert_allclose(line.anchor, (3.0, 0.0))
    np.testing.assert_allclose(line.start, (3.0, -6.0))
    np.testing.assert_allclose(line.end, (3.0, 6.0))
    np.testing.assert_allclose(line.end - line.start, 4.0 * line.direction)


def test_independence_is_detected_without_rendering() -> None:
    assert TwoVectorSpan((1.0, 0.0), (0.0, 1.0)).generators_are_independent
    assert not TwoVectorSpan((1.0, 2.0), (2.0, 4.0)).generators_are_independent


def test_endpoint_family_accepts_coefficient_pairs() -> None:
    model = TwoVectorSpan((1.0, 0.0), (0.0, 2.0))
    endpoints = model.endpoints_for(((1.0, 2.0), (-3.0, 0.5)))
    np.testing.assert_allclose(endpoints, ((1.0, 4.0), (-3.0, 1.0)))
    assert endpoints.shape == (2, 2)


def test_arrays_are_defensive_and_read_only() -> None:
    source_u = np.array([2.0, 1.0])
    source_v = np.array([-1.0, 3.0])
    model = TwoVectorSpan(source_u, source_v)
    source_u[:] = 99.0
    source_v[:] = 99.0

    np.testing.assert_allclose(model.generator_u, (2.0, 1.0))
    np.testing.assert_allclose(model.generator_v, (-1.0, 3.0))
    assert not model.snapshot(1.0, 1.0).endpoint.flags.writeable


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        TwoVectorSpan((1.0, 2.0), (1.0, 2.0, 3.0))
    with pytest.raises(ValueError):
        TwoVectorSpan(((1.0, 2.0),), (1.0, 2.0))

    model = TwoVectorSpan((1.0, 0.0), (0.0, 1.0))
    with pytest.raises(TypeError):
        model.snapshot("1", 2.0)
    with pytest.raises(ValueError):
        model.fixed_u_line(0.0, 2.0, -2.0)
    with pytest.raises(ValueError):
        model.endpoints_for((1.0, 2.0))
