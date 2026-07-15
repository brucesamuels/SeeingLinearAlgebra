from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import DecimalNumber, VGroup

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry import LinearCombinationGeometry
from engine.linear_combination_geometry_display import (
    LinearCombinationGeometryDisplayAdapter,
)
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath
from engine.manim_linear_combination_geometry import ManimLinearCombinationGeometry
from engine.manim_linear_combination_presentation import (
    ManimLinearCombinationPresentation,
)
from engine.manim_linear_combination_readout import ManimLinearCombinationReadout
from engine.rank_collapse_display import LinearDisplayProjector


@dataclass(frozen=True)
class MathematicalSnapshot:
    coefficients: object
    result: object


@dataclass(frozen=True)
class DisplaySnapshot:
    display_term_segments: object
    display_resultant_segment: object
    linear_combination_snapshot: object


def build_display_path(
    vectors=((2.0, 1.0), (-1.0, 2.0)),
    start=(0.0, 0.0),
    end=(1.25, -0.75),
    projection_matrix=None,
) -> LinearCombinationGeometryDisplayAdapter:
    combination = LinearCombination(vectors)
    coefficient_path = CoefficientSweepPath(combination, start, end)
    geometry_path = LinearCombinationGeometryPath(
        coefficient_path,
        LinearCombinationGeometry(),
    )
    if projection_matrix is None:
        projection_matrix = np.eye(combination.dimension, dtype=float)
    projector = LinearDisplayProjector(projection_matrix)
    return LinearCombinationGeometryDisplayAdapter(geometry_path, projector)


def entry_values(entries: tuple[DecimalNumber, ...]) -> np.ndarray:
    return np.array([entry.get_value() for entry in entries], dtype=float)


def endpoint_state(
    presentation: ManimLinearCombinationPresentation,
) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    arrows = (*presentation.geometry.term_arrows, presentation.geometry.resultant_arrow)
    return tuple((arrow.get_start().copy(), arrow.get_end().copy()) for arrow in arrows)


def test_adapter_consumes_actual_display_snapshot() -> None:
    display_path = build_display_path()
    snapshot = display_path.snapshot(0.5)

    presentation = ManimLinearCombinationPresentation(snapshot)

    assert presentation.snapshot is snapshot
    assert presentation.geometry.term_count == 2
    assert presentation.readout.snapshot is snapshot.linear_combination_snapshot
    np.testing.assert_allclose(
        entry_values(presentation.readout.coefficient_entries),
        snapshot.linear_combination_snapshot.coefficients,
    )
    np.testing.assert_allclose(
        presentation.geometry.resultant_arrow.get_end(),
        [*snapshot.display_resultant_end, 0.0],
    )


def test_adapter_is_root_vgroup_with_exact_two_children() -> None:
    snapshot = build_display_path().snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(snapshot)

    assert isinstance(presentation, VGroup)
    assert presentation.mobject is presentation
    assert isinstance(presentation.geometry, ManimLinearCombinationGeometry)
    assert isinstance(presentation.readout, ManimLinearCombinationReadout)
    assert presentation.submobjects == [presentation.geometry, presentation.readout]


def test_structural_properties_match_actual_snapshot() -> None:
    snapshot = build_display_path().snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(snapshot)

    assert presentation.vector_count == 2
    assert presentation.coefficient_count == 2
    assert presentation.display_dimension == 2
    assert presentation.result_dimension == 2


def test_update_synchronizes_both_children_from_one_snapshot() -> None:
    display_path = build_display_path()
    initial = display_path.snapshot(0.0)
    later = display_path.snapshot(0.625)
    presentation = ManimLinearCombinationPresentation(initial)

    returned = presentation.update_from_snapshot(later)

    assert returned is presentation
    assert presentation.snapshot is later
    assert presentation.readout.snapshot is later.linear_combination_snapshot
    np.testing.assert_allclose(
        entry_values(presentation.readout.coefficient_entries),
        later.linear_combination_snapshot.coefficients,
    )
    np.testing.assert_allclose(
        entry_values(presentation.readout.result_entries),
        later.linear_combination_snapshot.result,
    )
    np.testing.assert_allclose(
        presentation.geometry.resultant_arrow.get_end(),
        [*later.display_resultant_end, 0.0],
    )


def test_update_preserves_all_component_and_entry_identities() -> None:
    display_path = build_display_path()
    presentation = ManimLinearCombinationPresentation(display_path.snapshot(0.0))
    identities = {
        "root": id(presentation),
        "geometry": id(presentation.geometry),
        "terms": tuple(id(arrow) for arrow in presentation.geometry.term_arrows),
        "resultant": id(presentation.geometry.resultant_arrow),
        "readout": id(presentation.readout),
        "coefficient_entries": tuple(
            id(entry) for entry in presentation.readout.coefficient_entries
        ),
        "result_entries": tuple(
            id(entry) for entry in presentation.readout.result_entries
        ),
    }

    presentation.update_from_snapshot(display_path.snapshot(1.0))

    assert id(presentation) == identities["root"]
    assert id(presentation.geometry) == identities["geometry"]
    term_ids = tuple(id(arrow) for arrow in presentation.geometry.term_arrows)
    assert term_ids == identities["terms"]
    assert id(presentation.geometry.resultant_arrow) == identities["resultant"]
    assert id(presentation.readout) == identities["readout"]
    assert tuple(
        id(entry) for entry in presentation.readout.coefficient_entries
    ) == identities["coefficient_entries"]
    result_entry_ids = tuple(
        id(entry) for entry in presentation.readout.result_entries
    )
    assert result_entry_ids == identities["result_entries"]


def test_update_preserves_independent_readout_positioning() -> None:
    display_path = build_display_path()
    presentation = ManimLinearCombinationPresentation(display_path.snapshot(0.0))
    presentation.readout.shift(np.array([3.0, 2.0, 0.0]))
    entries = (
        *presentation.readout.coefficient_entries,
        *presentation.readout.result_entries,
    )
    centers_before = tuple(entry.get_center().copy() for entry in entries)

    presentation.update_from_snapshot(display_path.snapshot(1.0))

    for before, entry in zip(centers_before, entries, strict=True):
        np.testing.assert_allclose(entry.get_center(), before)


def test_geometry_and_readout_options_are_forwarded() -> None:
    snapshot = build_display_path().snapshot(1.0)
    geometry_kwargs = {
        "term_arrow_kwargs": {"stroke_width": 7.0},
        "resultant_arrow_kwargs": {"stroke_width": 9.0},
    }
    readout_kwargs = {
        "num_decimal_places": 3,
        "include_sign": False,
        "label_kwargs": {"font_size": 31},
    }

    presentation = ManimLinearCombinationPresentation(
        snapshot,
        geometry_kwargs=geometry_kwargs,
        readout_kwargs=readout_kwargs,
    )

    np.testing.assert_allclose(
        presentation.geometry.term_arrows[0].get_stroke_width(),
        7.0,
    )
    np.testing.assert_allclose(
        presentation.geometry.resultant_arrow.get_stroke_width(),
        9.0,
    )
    assert presentation.readout.coefficient_label_mobject.font_size == pytest.approx(
        31.0
    )
    assert presentation.readout.result_label_mobject.font_size == pytest.approx(
        31.0
    )
    assert geometry_kwargs == {
        "term_arrow_kwargs": {"stroke_width": 7.0},
        "resultant_arrow_kwargs": {"stroke_width": 9.0},
    }
    assert readout_kwargs == {
        "num_decimal_places": 3,
        "include_sign": False,
        "label_kwargs": {"font_size": 31},
    }


def test_higher_dimensional_mathematics_can_project_to_two_dimensions() -> None:
    display_path = build_display_path(
        vectors=((1.0, 2.0, 3.0), (-2.0, 1.0, 4.0)),
        start=(0.0, 0.0),
        end=(0.5, -1.0),
        projection_matrix=np.array(
            [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
            dtype=float,
        ),
    )
    snapshot = display_path.snapshot(1.0)
    presentation = ManimLinearCombinationPresentation(snapshot)

    assert presentation.display_dimension == 2
    assert presentation.result_dimension == 3
    np.testing.assert_allclose(
        entry_values(presentation.readout.result_entries),
        snapshot.linear_combination_snapshot.result,
    )


def test_three_dimensional_display_is_supported() -> None:
    display_path = build_display_path(
        vectors=((1.0, 2.0, 3.0), (-2.0, 1.0, 4.0)),
        start=(0.0, 0.0),
        end=(0.5, -1.0),
        projection_matrix=np.eye(3, dtype=float),
    )
    snapshot = display_path.snapshot(1.0)
    presentation = ManimLinearCombinationPresentation(snapshot)

    assert presentation.display_dimension == 3
    np.testing.assert_allclose(
        presentation.geometry.resultant_arrow.get_end(),
        snapshot.display_resultant_end,
    )


def test_missing_canonical_display_fields_are_rejected() -> None:
    with pytest.raises(TypeError, match="display_term_segments"):
        ManimLinearCombinationPresentation(object())  # type: ignore[arg-type]


def test_term_and_coefficient_counts_must_agree_at_construction() -> None:
    snapshot = DisplaySnapshot(
        display_term_segments=np.zeros((2, 2, 2)),
        display_resultant_segment=np.zeros((2, 2)),
        linear_combination_snapshot=MathematicalSnapshot(
            coefficients=np.zeros(3),
            result=np.zeros(2),
        ),
    )

    with pytest.raises(ValueError, match="term-arrow count must equal"):
        ManimLinearCombinationPresentation(snapshot)


def test_changed_term_count_is_rejected_before_any_mobject_mutates() -> None:
    display_path = build_display_path()
    initial = display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    old_endpoints = endpoint_state(presentation)
    old_coefficients = entry_values(presentation.readout.coefficient_entries)
    changed = DisplaySnapshot(
        display_term_segments=np.zeros((3, 2, 2)),
        display_resultant_segment=np.zeros((2, 2)),
        linear_combination_snapshot=MathematicalSnapshot(
            coefficients=np.zeros(3),
            result=np.zeros(2),
        ),
    )

    with pytest.raises(ValueError, match="term-arrow count changed"):
        presentation.update_from_snapshot(changed)

    assert presentation.snapshot is initial
    for (old_start, old_end), arrow in zip(
        old_endpoints,
        (*presentation.geometry.term_arrows, presentation.geometry.resultant_arrow),
        strict=True,
    ):
        np.testing.assert_allclose(arrow.get_start(), old_start)
        np.testing.assert_allclose(arrow.get_end(), old_end)
    np.testing.assert_allclose(
        entry_values(presentation.readout.coefficient_entries),
        old_coefficients,
    )


def test_changed_display_dimension_is_rejected_before_any_mobject_mutates() -> None:
    initial = build_display_path().snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    old_endpoints = endpoint_state(presentation)
    changed = DisplaySnapshot(
        display_term_segments=np.zeros((2, 2, 3)),
        display_resultant_segment=np.zeros((2, 3)),
        linear_combination_snapshot=MathematicalSnapshot(
            coefficients=np.zeros(2),
            result=np.zeros(2),
        ),
    )

    with pytest.raises(ValueError, match="display dimension changed"):
        presentation.update_from_snapshot(changed)

    assert presentation.snapshot is initial
    for (old_start, old_end), arrow in zip(
        old_endpoints,
        (*presentation.geometry.term_arrows, presentation.geometry.resultant_arrow),
        strict=True,
    ):
        np.testing.assert_allclose(arrow.get_start(), old_start)
        np.testing.assert_allclose(arrow.get_end(), old_end)


def test_changed_result_dimension_is_rejected_before_any_mobject_mutates() -> None:
    initial = build_display_path().snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    old_endpoints = endpoint_state(presentation)
    old_result = entry_values(presentation.readout.result_entries)
    changed = DisplaySnapshot(
        display_term_segments=np.zeros((2, 2, 2)),
        display_resultant_segment=np.zeros((2, 2)),
        linear_combination_snapshot=MathematicalSnapshot(
            coefficients=np.zeros(2),
            result=np.zeros(3),
        ),
    )

    with pytest.raises(ValueError, match="result dimension changed"):
        presentation.update_from_snapshot(changed)

    assert presentation.snapshot is initial
    for (old_start, old_end), arrow in zip(
        old_endpoints,
        (*presentation.geometry.term_arrows, presentation.geometry.resultant_arrow),
        strict=True,
    ):
        np.testing.assert_allclose(arrow.get_start(), old_start)
        np.testing.assert_allclose(arrow.get_end(), old_end)
    np.testing.assert_allclose(
        entry_values(presentation.readout.result_entries),
        old_result,
    )


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
def test_nonfinite_incoming_values_are_rejected_before_mutation(
    bad_value: float,
) -> None:
    initial = build_display_path().snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    old_endpoints = endpoint_state(presentation)
    old_coefficients = entry_values(presentation.readout.coefficient_entries)
    terms = np.zeros((2, 2, 2), dtype=float)
    terms[0, 1, 0] = bad_value
    changed = DisplaySnapshot(
        display_term_segments=terms,
        display_resultant_segment=np.zeros((2, 2)),
        linear_combination_snapshot=MathematicalSnapshot(
            coefficients=np.zeros(2),
            result=np.zeros(2),
        ),
    )

    with pytest.raises(ValueError, match="finite"):
        presentation.update_from_snapshot(changed)

    assert presentation.snapshot is initial
    for (old_start, old_end), arrow in zip(
        old_endpoints,
        (*presentation.geometry.term_arrows, presentation.geometry.resultant_arrow),
        strict=True,
    ):
        np.testing.assert_allclose(arrow.get_start(), old_start)
        np.testing.assert_allclose(arrow.get_end(), old_end)
    np.testing.assert_allclose(
        entry_values(presentation.readout.coefficient_entries),
        old_coefficients,
    )


@pytest.mark.parametrize("argument", ["geometry_kwargs", "readout_kwargs"])
def test_component_options_cannot_override_snapshot(argument: str) -> None:
    snapshot = build_display_path().snapshot(0.0)

    with pytest.raises(ValueError, match="adapter-owned snapshot"):
        ManimLinearCombinationPresentation(
            snapshot,
            **{argument: {"snapshot": object()}},
        )
