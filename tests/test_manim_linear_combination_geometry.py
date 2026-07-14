from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import Arrow, VGroup

from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)


@dataclass(frozen=True)
class ArrowSnapshot:
    start: tuple[float, ...]
    end: tuple[float, ...]


@dataclass(frozen=True)
class DisplaySnapshot:
    term_arrows: tuple[ArrowSnapshot, ...]
    resultant_arrow: ArrowSnapshot


def snapshot_one() -> DisplaySnapshot:
    return DisplaySnapshot(
        term_arrows=(
            ArrowSnapshot((0.0, 0.0), (2.0, 1.0)),
            ArrowSnapshot((2.0, 1.0), (1.0, 3.0)),
        ),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (1.0, 3.0)),
    )


def snapshot_two() -> DisplaySnapshot:
    return DisplaySnapshot(
        term_arrows=(
            ArrowSnapshot((0.0, 0.0), (-1.0, 2.0)),
            ArrowSnapshot((-1.0, 2.0), (3.0, 1.0)),
        ),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (3.0, 1.0)),
    )


def test_creates_one_fixed_manim_arrow_per_displayed_arrow() -> None:
    adapter = ManimLinearCombinationGeometry(snapshot_one())

    assert isinstance(adapter, VGroup)
    assert adapter.mobject is adapter
    assert adapter.term_count == 2
    assert all(isinstance(arrow, Arrow) for arrow in adapter.term_arrows)
    assert isinstance(adapter.resultant_arrow, Arrow)
    assert tuple(adapter.submobjects) == (
        *adapter.term_arrows,
        adapter.resultant_arrow,
    )


def test_two_dimensional_display_points_are_embedded_in_manim_space() -> None:
    adapter = ManimLinearCombinationGeometry(snapshot_one())

    np.testing.assert_allclose(adapter.term_arrows[0].get_start(), (0.0, 0.0, 0.0))
    np.testing.assert_allclose(adapter.term_arrows[0].get_end(), (2.0, 1.0, 0.0))
    np.testing.assert_allclose(adapter.resultant_arrow.get_end(), (1.0, 3.0, 0.0))


def test_update_preserves_every_mobject_identity() -> None:
    adapter = ManimLinearCombinationGeometry(snapshot_one())
    term_ids = tuple(id(arrow) for arrow in adapter.term_arrows)
    resultant_id = id(adapter.resultant_arrow)
    root_id = id(adapter)

    returned = adapter.update_from_snapshot(snapshot_two())

    assert returned is adapter
    assert id(adapter) == root_id
    assert tuple(id(arrow) for arrow in adapter.term_arrows) == term_ids
    assert id(adapter.resultant_arrow) == resultant_id
    np.testing.assert_allclose(adapter.term_arrows[0].get_start(), (0.0, 0.0, 0.0))
    np.testing.assert_allclose(adapter.term_arrows[0].get_end(), (-1.0, 2.0, 0.0))
    np.testing.assert_allclose(adapter.term_arrows[1].get_start(), (-1.0, 2.0, 0.0))
    np.testing.assert_allclose(adapter.term_arrows[1].get_end(), (3.0, 1.0, 0.0))
    np.testing.assert_allclose(adapter.resultant_arrow.get_end(), (3.0, 1.0, 0.0))


def test_changed_term_count_is_rejected_before_any_arrow_mutates() -> None:
    adapter = ManimLinearCombinationGeometry(snapshot_one())
    old_endpoints = tuple(
        (arrow.get_start().copy(), arrow.get_end().copy())
        for arrow in (*adapter.term_arrows, adapter.resultant_arrow)
    )
    changed_count = DisplaySnapshot(
        term_arrows=(ArrowSnapshot((0.0, 0.0), (1.0, 0.0)),),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (1.0, 0.0)),
    )

    with pytest.raises(ValueError, match="term-arrow count changed"):
        adapter.update_from_snapshot(changed_count)

    new_endpoints = tuple(
        (arrow.get_start(), arrow.get_end())
        for arrow in (*adapter.term_arrows, adapter.resultant_arrow)
    )
    for (old_start, old_end), (new_start, new_end) in zip(
        old_endpoints,
        new_endpoints,
        strict=True,
    ):
        np.testing.assert_allclose(new_start, old_start)
        np.testing.assert_allclose(new_end, old_end)


def test_zero_length_arrow_remains_finite_and_can_later_expand_in_place() -> None:
    zero_snapshot = DisplaySnapshot(
        term_arrows=(ArrowSnapshot((1.0, -2.0), (1.0, -2.0)),),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (0.0, 0.0)),
    )
    adapter = ManimLinearCombinationGeometry(zero_snapshot)
    term_id = id(adapter.term_arrows[0])
    resultant_id = id(adapter.resultant_arrow)

    assert np.all(np.isfinite(adapter.term_arrows[0].points))
    assert adapter.term_arrows[0].get_length() <= 1.0e-7
    assert adapter.resultant_arrow.get_length() <= 1.0e-7

    nonzero_snapshot = DisplaySnapshot(
        term_arrows=(ArrowSnapshot((1.0, -2.0), (4.0, 2.0)),),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (3.0, 4.0)),
    )
    adapter.update_from_snapshot(nonzero_snapshot)

    assert id(adapter.term_arrows[0]) == term_id
    assert id(adapter.resultant_arrow) == resultant_id
    np.testing.assert_allclose(adapter.term_arrows[0].get_end(), (4.0, 2.0, 0.0))
    np.testing.assert_allclose(adapter.resultant_arrow.get_end(), (3.0, 4.0, 0.0))


def test_arrow_style_mappings_are_copied_and_buff_is_fixed_at_zero() -> None:
    term_style = {"stroke_width": 3.0}
    result_style = {"stroke_width": 7.0, "buff": 0.0}

    adapter = ManimLinearCombinationGeometry(
        snapshot_one(),
        term_arrow_kwargs=term_style,
        resultant_arrow_kwargs=result_style,
    )

    assert term_style == {"stroke_width": 3.0}
    assert result_style == {"stroke_width": 7.0, "buff": 0.0}
    np.testing.assert_allclose(adapter.term_arrows[0].get_start(), (0.0, 0.0, 0.0))
    np.testing.assert_allclose(adapter.term_arrows[0].get_end(), (2.0, 1.0, 0.0))


def test_nonzero_buff_is_rejected_because_it_changes_projected_geometry() -> None:
    with pytest.raises(ValueError, match="buff must be zero"):
        ManimLinearCombinationGeometry(
            snapshot_one(),
            term_arrow_kwargs={"buff": 0.25},
        )


def test_invalid_display_dimension_is_rejected() -> None:
    invalid = DisplaySnapshot(
        term_arrows=(ArrowSnapshot((0.0,), (1.0,)),),
        resultant_arrow=ArrowSnapshot((0.0, 0.0), (1.0, 0.0)),
    )

    with pytest.raises(ValueError, match="two or three coordinates"):
        ManimLinearCombinationGeometry(invalid)
