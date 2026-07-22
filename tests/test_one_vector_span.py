import numpy as np
import pytest

from engine.one_vector_span import OneVectorSpan


def test_scalar_multiple_snapshot_is_exact() -> None:
    model = OneVectorSpan((2.0, -1.0))
    snapshot = model.snapshot(3.5)

    assert snapshot.coefficient == 3.5
    np.testing.assert_allclose(snapshot.generator, (2.0, -1.0))
    np.testing.assert_allclose(snapshot.endpoint, (7.0, -3.5))
    assert snapshot.dimension == 2


def test_negative_and_zero_coefficients_remain_in_the_same_span() -> None:
    model = OneVectorSpan((3.0, 2.0))

    np.testing.assert_allclose(model.snapshot(-2.0).endpoint, (-6.0, -4.0))
    np.testing.assert_allclose(model.snapshot(0.0).endpoint, (0.0, 0.0))
    assert model.snapshot(0.0).is_zero_vector


def test_endpoint_family_has_one_row_per_coefficient() -> None:
    model = OneVectorSpan((2.0, 1.0))
    endpoints = model.endpoints_for((-2.0, 0.0, 1.5))

    np.testing.assert_allclose(endpoints, ((-4.0, -2.0), (0.0, 0.0), (3.0, 1.5)))
    assert endpoints.shape == (3, 2)


def test_model_is_dimension_independent() -> None:
    model = OneVectorSpan((1.0, -2.0, 4.0))
    snapshot = model.snapshot(-0.5)

    assert model.dimension == 3
    np.testing.assert_allclose(snapshot.endpoint, (-0.5, 1.0, -2.0))


def test_generator_and_snapshots_are_defensive_read_only_arrays() -> None:
    source = np.array([2.0, 1.0])
    model = OneVectorSpan(source)
    source[:] = 99.0

    np.testing.assert_allclose(model.generator, (2.0, 1.0))
    assert not model.generator.flags.writeable
    assert not model.snapshot(2.0).endpoint.flags.writeable


def test_invalid_generator_or_coefficient_is_rejected() -> None:
    with pytest.raises(ValueError):
        OneVectorSpan(())
    with pytest.raises(ValueError):
        OneVectorSpan(((1.0, 2.0),))
    with pytest.raises(ValueError):
        OneVectorSpan((1.0, np.inf))

    model = OneVectorSpan((1.0, 2.0))
    with pytest.raises(TypeError):
        model.snapshot("2")
    with pytest.raises(ValueError):
        model.snapshot(np.nan)
