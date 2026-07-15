"""Focused tests for reusable Manim linear-combination labels."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

manim = pytest.importorskip("manim")

from manim import MathTex, VGroup  # noqa: E402

from engine.coefficient_sweep_path import CoefficientSweepPath  # noqa: E402
from engine.linear_combination import LinearCombination  # noqa: E402
from engine.linear_combination_geometry import LinearCombinationGeometry  # noqa: E402
from engine.linear_combination_geometry_display import (  # noqa: E402
    LinearCombinationGeometryDisplayAdapter,
)
from engine.linear_combination_geometry_path import (  # noqa: E402
    LinearCombinationGeometryPath,
)
from engine.rank_collapse_display import LinearDisplayProjector  # noqa: E402
from engine.manim_linear_combination_labels import (  # noqa: E402
    ManimLinearCombinationLabels,
)


@dataclass(frozen=True)
class DisplaySnapshot:
    """Small canonical display-snapshot test double for invalid cases."""

    display_term_segments: np.ndarray
    display_resultant_segment: np.ndarray


def _display_path(
    *,
    vectors: np.ndarray | None = None,
    start_coefficients: np.ndarray | None = None,
    end_coefficients: np.ndarray | None = None,
    display_dimension: int = 2,
) -> LinearCombinationGeometryDisplayAdapter:
    if vectors is None:
        vectors = np.array(
            [
                [2.0, 1.0],
                [-1.0, 2.0],
            ]
        )
    if start_coefficients is None:
        start_coefficients = np.zeros(vectors.shape[0])
    if end_coefficients is None:
        end_coefficients = np.array([1.25, -0.75])

    combination = LinearCombination(vectors)
    coefficient_path = CoefficientSweepPath(
        combination,
        start_coefficients,
        end_coefficients,
    )
    geometry_path = LinearCombinationGeometryPath(
        coefficient_path,
        LinearCombinationGeometry(),
    )
    projection_matrix = np.eye(
        display_dimension,
        combination.dimension,
        dtype=float,
    )
    projector = LinearDisplayProjector(projection_matrix)
    return LinearCombinationGeometryDisplayAdapter(geometry_path, projector)


def _centers(labels: ManimLinearCombinationLabels) -> tuple[np.ndarray, ...]:
    return tuple(
        np.array(label.get_center(), dtype=float)
        for label in (
            *labels.term_label_mobjects,
            labels.resultant_label_mobject,
        )
    )


def _expected_centers(
    snapshot: object,
    *,
    term_offset: np.ndarray,
    resultant_offset: np.ndarray,
) -> tuple[np.ndarray, ...]:
    term_segments = np.asarray(snapshot.display_term_segments, dtype=float)
    resultant_segment = np.asarray(
        snapshot.display_resultant_segment,
        dtype=float,
    )

    def embed(point: np.ndarray) -> np.ndarray:
        embedded = np.zeros(3)
        embedded[: point.size] = point
        return embedded

    term_centers = tuple(
        embed(np.mean(segment, axis=0)) + term_offset
        for segment in term_segments
    )
    resultant_center = (
        embed(np.mean(resultant_segment, axis=0)) + resultant_offset
    )
    return (*term_centers, resultant_center)


def test_labels_consume_actual_display_snapshot_and_use_midpoint_anchors() -> None:
    snapshot = _display_path().snapshot(0.5)

    labels = ManimLinearCombinationLabels(snapshot)

    assert isinstance(labels, VGroup)
    assert labels.mobject is labels
    assert labels.snapshot is snapshot
    assert labels.term_count == 2
    assert labels.display_dimension == 2
    assert labels.term_label_sources == (
        r"c_{1}\mathbf{v}_{1}",
        r"c_{2}\mathbf{v}_{2}",
    )
    assert labels.resultant_label_source == r"\mathbf{r}"
    assert all(
        isinstance(label, MathTex) for label in labels.term_label_mobjects
    )
    assert isinstance(labels.resultant_label_mobject, MathTex)

    expected = _expected_centers(
        snapshot,
        term_offset=np.array([0.0, 0.25, 0.0]),
        resultant_offset=np.array([0.0, -0.25, 0.0]),
    )
    for actual, target in zip(_centers(labels), expected, strict=True):
        np.testing.assert_allclose(actual, target)


def test_root_group_contains_exact_fixed_labels_in_public_order() -> None:
    labels = ManimLinearCombinationLabels(_display_path().snapshot(0.0))

    assert tuple(labels.submobjects) == (
        *labels.term_label_mobjects,
        labels.resultant_label_mobject,
    )


def test_update_preserves_all_label_identities_and_retains_exact_snapshot() -> None:
    display_path = _display_path()
    initial_snapshot = display_path.snapshot(0.0)
    later_snapshot = display_path.snapshot(0.8)
    labels = ManimLinearCombinationLabels(initial_snapshot)

    root_identity = id(labels)
    term_identities = tuple(id(label) for label in labels.term_label_mobjects)
    resultant_identity = id(labels.resultant_label_mobject)
    before_centers = _centers(labels)

    returned = labels.update_from_snapshot(later_snapshot)

    assert returned is labels
    assert id(labels) == root_identity
    assert tuple(id(label) for label in labels.term_label_mobjects) == term_identities
    assert id(labels.resultant_label_mobject) == resultant_identity
    assert labels.snapshot is later_snapshot
    assert any(
        not np.allclose(before, after)
        for before, after in zip(before_centers, _centers(labels), strict=True)
    )

    expected = _expected_centers(
        later_snapshot,
        term_offset=labels.term_label_offset,
        resultant_offset=labels.resultant_label_offset,
    )
    for actual, target in zip(_centers(labels), expected, strict=True):
        np.testing.assert_allclose(actual, target)


def test_custom_sources_offsets_and_options_are_copied_and_observable() -> None:
    snapshot = _display_path().snapshot(0.4)
    term_sources = [r"a\mathbf{u}", r"b\mathbf{w}"]
    label_options = {"font_size": 31.0}

    labels = ManimLinearCombinationLabels(
        snapshot,
        term_labels=term_sources,
        resultant_label=r"\mathbf{s}",
        term_label_offset=(0.5, 0.1),
        resultant_label_offset=(-0.25, -0.4, 0.0),
        label_kwargs=label_options,
    )

    term_sources.append(r"unexpected")
    label_options["font_size"] = 99.0

    assert labels.term_label_sources == (
        r"a\mathbf{u}",
        r"b\mathbf{w}",
    )
    assert labels.resultant_label_source == r"\mathbf{s}"
    np.testing.assert_allclose(labels.term_label_offset, [0.5, 0.1, 0.0])
    np.testing.assert_allclose(
        labels.resultant_label_offset,
        [-0.25, -0.4, 0.0],
    )
    assert all(label.font_size == pytest.approx(31.0) for label in labels)

    expected = _expected_centers(
        snapshot,
        term_offset=np.array([0.5, 0.1, 0.0]),
        resultant_offset=np.array([-0.25, -0.4, 0.0]),
    )
    for actual, target in zip(_centers(labels), expected, strict=True):
        np.testing.assert_allclose(actual, target)


def test_three_dimensional_display_coordinates_are_preserved() -> None:
    vectors = np.array(
        [
            [2.0, 1.0, -0.5],
            [-1.0, 2.0, 1.5],
        ]
    )
    snapshot = _display_path(
        vectors=vectors,
        end_coefficients=np.array([0.75, -1.25]),
        display_dimension=3,
    ).snapshot(0.6)

    labels = ManimLinearCombinationLabels(
        snapshot,
        term_label_offset=(0.0, 0.0, 0.2),
        resultant_label_offset=(0.0, 0.0, -0.2),
    )

    assert labels.display_dimension == 3
    expected = _expected_centers(
        snapshot,
        term_offset=np.array([0.0, 0.0, 0.2]),
        resultant_offset=np.array([0.0, 0.0, -0.2]),
    )
    for actual, target in zip(_centers(labels), expected, strict=True):
        np.testing.assert_allclose(actual, target)


@pytest.mark.parametrize(
    ("snapshot", "message"),
    [
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((3, 2, 2)),
                display_resultant_segment=np.zeros((2, 2)),
            ),
            "term count",
        ),
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((2, 2, 3)),
                display_resultant_segment=np.zeros((2, 3)),
            ),
            "display dimension",
        ),
        (
            DisplaySnapshot(
                display_term_segments=np.array(
                    [
                        [[0.0, 0.0], [1.0, 1.0]],
                        [[1.0, 1.0], [np.nan, 2.0]],
                    ]
                ),
                display_resultant_segment=np.zeros((2, 2)),
            ),
            "finite",
        ),
    ],
)
def test_structurally_invalid_updates_are_rejected_atomically(
    snapshot: DisplaySnapshot,
    message: str,
) -> None:
    initial_snapshot = _display_path().snapshot(0.25)
    labels = ManimLinearCombinationLabels(initial_snapshot)
    centers_before = _centers(labels)

    with pytest.raises(ValueError, match=message):
        labels.update_from_snapshot(snapshot)

    assert labels.snapshot is initial_snapshot
    for before, after in zip(centers_before, _centers(labels), strict=True):
        np.testing.assert_allclose(after, before)


def test_missing_canonical_display_fields_are_rejected() -> None:
    class MissingDisplayFields:
        pass

    with pytest.raises(TypeError, match="display_term_segments"):
        ManimLinearCombinationLabels(MissingDisplayFields())


@pytest.mark.parametrize(
    ("snapshot", "message"),
    [
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((2, 2)),
                display_resultant_segment=np.zeros((2, 2)),
            ),
            "shape",
        ),
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((0, 2, 2)),
                display_resultant_segment=np.zeros((2, 2)),
            ),
            "at least one",
        ),
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((2, 2, 4)),
                display_resultant_segment=np.zeros((2, 4)),
            ),
            "dimension",
        ),
        (
            DisplaySnapshot(
                display_term_segments=np.zeros((2, 2, 2)),
                display_resultant_segment=np.zeros((3, 2)),
            ),
            "resultant",
        ),
    ],
)
def test_invalid_snapshot_shapes_are_rejected(
    snapshot: DisplaySnapshot,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        ManimLinearCombinationLabels(snapshot)


@pytest.mark.parametrize(
    ("term_labels", "exception", "message"),
    [
        ((r"only-one",), ValueError, "length"),
        (r"not-a-sequence-of-labels", TypeError, "sequence"),
        ((r"valid", 2), TypeError, "must be a string"),
        ((r"valid", "   "), ValueError, "must not be empty"),
    ],
)
def test_invalid_term_label_sources_are_rejected(
    term_labels: object,
    exception: type[Exception],
    message: str,
) -> None:
    with pytest.raises(exception, match=message):
        ManimLinearCombinationLabels(
            _display_path().snapshot(0.0),
            term_labels=term_labels,
        )


@pytest.mark.parametrize(
    ("resultant_label", "exception", "message"),
    [
        (3, TypeError, "must be a string"),
        ("", ValueError, "must not be empty"),
    ],
)
def test_invalid_resultant_label_source_is_rejected(
    resultant_label: object,
    exception: type[Exception],
    message: str,
) -> None:
    with pytest.raises(exception, match=message):
        ManimLinearCombinationLabels(
            _display_path().snapshot(0.0),
            resultant_label=resultant_label,
        )


@pytest.mark.parametrize(
    ("keyword", "value", "exception", "message"),
    [
        ("term_label_offset", (1.0,), ValueError, "2 or 3"),
        ("term_label_offset", (1.0, 2.0, 3.0, 4.0), ValueError, "2 or 3"),
        ("resultant_label_offset", (0.0, np.inf), ValueError, "finite"),
        ("resultant_label_offset", "up", TypeError, "numeric"),
    ],
)
def test_invalid_offsets_are_rejected(
    keyword: str,
    value: object,
    exception: type[Exception],
    message: str,
) -> None:
    with pytest.raises(exception, match=message):
        ManimLinearCombinationLabels(
            _display_path().snapshot(0.0),
            **{keyword: value},
        )


def test_label_options_must_be_a_mapping_and_cannot_replace_text() -> None:
    snapshot = _display_path().snapshot(0.0)

    with pytest.raises(TypeError, match="mapping"):
        ManimLinearCombinationLabels(snapshot, label_kwargs=[("font_size", 30)])

    with pytest.raises(ValueError, match="label text"):
        ManimLinearCombinationLabels(
            snapshot,
            label_kwargs={"tex_strings": (r"x",)},
        )
