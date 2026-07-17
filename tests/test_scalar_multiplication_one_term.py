from __future__ import annotations

import inspect

import numpy as np
import pytest

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry import LinearCombinationGeometry
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath


VECTOR = np.array([2.0, -3.0])
START_COEFFICIENTS = np.array([-1.5])
END_COEFFICIENTS = np.array([2.0])


def _construct_linear_combination() -> LinearCombination:
    """Construct the existing engine through its public parameter names."""
    signature = inspect.signature(LinearCombination)
    parameters = signature.parameters

    candidates = {
        "vectors": np.array([VECTOR]),
        "basis_vectors": np.array([VECTOR]),
        "source_vectors": np.array([VECTOR]),
        "terms": np.array([VECTOR]),
        "vector_matrix": np.array([VECTOR]),
    }

    kwargs = {
        name: value
        for name, value in candidates.items()
        if name in parameters
    }
    if kwargs:
        return LinearCombination(**kwargs)

    # The established API may use one positional vector-array argument.
    required = [
        parameter
        for parameter in parameters.values()
        if parameter.name != "self"
        and parameter.default is inspect.Parameter.empty
        and parameter.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]
    if len(required) == 1:
        return LinearCombination(np.array([VECTOR]))

    raise AssertionError(
        "Unable to identify the public LinearCombination constructor. "
        f"Signature: {signature}"
    )


def _snapshot(model: LinearCombination, coefficients: np.ndarray):
    for method_name in ("snapshot", "evaluate", "at"):
        method = getattr(model, method_name, None)
        if callable(method):
            return method(coefficients)
    raise AssertionError(
        "LinearCombination exposes none of snapshot/evaluate/at"
    )



def _construct_coefficient_path(
    model: LinearCombination,
) -> CoefficientSweepPath:
    return CoefficientSweepPath(
        model,
        START_COEFFICIENTS,
        END_COEFFICIENTS,
    )


def _coefficients_at(path: CoefficientSweepPath, progress: float) -> np.ndarray:
    return np.asarray(path.coefficients_at(progress), dtype=float)


def _construct_geometry() -> LinearCombinationGeometry:
    return LinearCombinationGeometry()


def _geometry_snapshot(
    geometry: LinearCombinationGeometry,
    model: LinearCombination,
    coefficients: np.ndarray,
):
    return geometry.snapshot(_snapshot(model, coefficients))


def test_one_term_snapshot_is_exact_scalar_multiplication() -> None:
    model = _construct_linear_combination()
    coefficients = np.array([-0.5])

    snapshot = _snapshot(model, coefficients)
    expected = coefficients[0] * VECTOR

    np.testing.assert_allclose(snapshot.coefficients, coefficients)
    assert snapshot.terms.shape == (1, 2)
    np.testing.assert_allclose(snapshot.terms[0], expected)
    np.testing.assert_allclose(snapshot.result, expected)
    assert snapshot.partial_sums.shape == (2, 2)
    np.testing.assert_allclose(snapshot.partial_sums[0], np.zeros(2))
    np.testing.assert_allclose(snapshot.partial_sums[1], expected)


@pytest.mark.parametrize(
    ("coefficient", "expected"),
    [
        (2.0, np.array([4.0, -6.0])),
        (0.5, np.array([1.0, -1.5])),
        (0.0, np.array([0.0, 0.0])),
        (-1.0, np.array([-2.0, 3.0])),
    ],
)
def test_one_term_case_covers_stretch_shrink_zero_and_reversal(
    coefficient: float,
    expected: np.ndarray,
) -> None:
    snapshot = _snapshot(
        _construct_linear_combination(),
        np.array([coefficient]),
    )
    np.testing.assert_allclose(snapshot.result, expected)


def test_one_term_coefficient_path_remains_shape_one() -> None:
    model = _construct_linear_combination()
    path = _construct_coefficient_path(model)

    for progress in (0.0, 0.25, 0.5, 0.75, 1.0):
        coefficients = _coefficients_at(path, progress)
        expected = (
            (1.0 - progress) * START_COEFFICIENTS
            + progress * END_COEFFICIENTS
        )
        assert coefficients.shape == (1,)
        np.testing.assert_allclose(coefficients, expected)


def test_one_term_geometry_is_one_origin_anchored_segment() -> None:
    model = _construct_linear_combination()
    geometry = _construct_geometry()
    coefficients = np.array([1.5])

    snapshot = _geometry_snapshot(geometry, model, coefficients)
    expected = coefficients[0] * VECTOR

    assert snapshot.term_segments.shape == (1, 2, 2)
    np.testing.assert_allclose(snapshot.term_segments[0, 0], np.zeros(2))
    np.testing.assert_allclose(snapshot.term_segments[0, 1], expected)
    np.testing.assert_allclose(
        snapshot.resultant_segment,
        np.array([np.zeros(2), expected]),
    )


def test_geometry_path_accepts_one_term_pipeline() -> None:
    model = _construct_linear_combination()
    geometry = _construct_geometry()
    coefficient_path = _construct_coefficient_path(model)

    path = LinearCombinationGeometryPath(coefficient_path, geometry)

    snapshot = path.snapshot(0.5)

    expected_coefficient = (
        0.5 * START_COEFFICIENTS[0]
        + 0.5 * END_COEFFICIENTS[0]
    )
    expected = expected_coefficient * VECTOR

    assert snapshot.term_segments.shape == (1, 2, 2)
    np.testing.assert_allclose(snapshot.term_segments[0, 1], expected)
    np.testing.assert_allclose(snapshot.resultant_segment[1], expected)
