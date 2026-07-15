from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

pytest.importorskip("manim")
from manim import DecimalMatrix, DecimalNumber, MathTex, RIGHT, VGroup

from engine.linear_combination import LinearCombination
from engine.manim_linear_combination_readout import ManimLinearCombinationReadout


@dataclass(frozen=True)
class ReadoutSnapshot:
    coefficients: object
    result: object


def entry_values(entries: tuple[DecimalNumber, ...]) -> np.ndarray:
    return np.array([entry.get_value() for entry in entries], dtype=float)


def make_snapshot(coefficients=(1.25, -0.75), result=(3.25, -0.25)):
    return ReadoutSnapshot(
        coefficients=np.asarray(coefficients, dtype=float),
        result=np.asarray(result, dtype=float),
    )


def test_adapter_consumes_actual_linear_combination_snapshot() -> None:
    snapshot = LinearCombination([[2.0, 1.0], [-1.0, 2.0]]).snapshot(
        [1.25, -0.75]
    )
    adapter = ManimLinearCombinationReadout(snapshot)

    assert adapter.snapshot is snapshot
    assert adapter.vector_count == 2
    assert adapter.dimension == 2
    np.testing.assert_allclose(entry_values(adapter.coefficient_entries), [1.25, -0.75])
    np.testing.assert_allclose(entry_values(adapter.result_entries), [3.25, -0.25])


def test_adapter_is_root_vgroup_and_exposes_fixed_components() -> None:
    adapter = ManimLinearCombinationReadout(make_snapshot())

    assert isinstance(adapter, VGroup)
    assert adapter.mobject is adapter
    assert isinstance(adapter.coefficient_label_mobject, MathTex)
    assert isinstance(adapter.result_label_mobject, MathTex)
    assert isinstance(adapter.coefficient_matrix, DecimalMatrix)
    assert isinstance(adapter.result_matrix, DecimalMatrix)
    assert all(isinstance(entry, DecimalNumber) for entry in adapter.coefficient_entries)
    assert all(isinstance(entry, DecimalNumber) for entry in adapter.result_entries)


def test_update_preserves_root_matrix_label_and_entry_identities() -> None:
    first = make_snapshot((0.0, 0.0), (0.0, 0.0))
    second = make_snapshot((1.25, -0.75), (3.25, -0.25))
    adapter = ManimLinearCombinationReadout(first)

    root_id = id(adapter)
    coefficient_matrix_id = id(adapter.coefficient_matrix)
    result_matrix_id = id(adapter.result_matrix)
    coefficient_label_id = id(adapter.coefficient_label_mobject)
    result_label_id = id(adapter.result_label_mobject)
    coefficient_entry_ids = tuple(id(entry) for entry in adapter.coefficient_entries)
    result_entry_ids = tuple(id(entry) for entry in adapter.result_entries)

    returned = adapter.update_from_snapshot(second)

    assert returned is adapter
    assert id(adapter) == root_id
    assert id(adapter.coefficient_matrix) == coefficient_matrix_id
    assert id(adapter.result_matrix) == result_matrix_id
    assert id(adapter.coefficient_label_mobject) == coefficient_label_id
    assert id(adapter.result_label_mobject) == result_label_id
    assert tuple(id(entry) for entry in adapter.coefficient_entries) == coefficient_entry_ids
    assert tuple(id(entry) for entry in adapter.result_entries) == result_entry_ids
    assert adapter.snapshot is second
    np.testing.assert_allclose(entry_values(adapter.coefficient_entries), [1.25, -0.75])
    np.testing.assert_allclose(entry_values(adapter.result_entries), [3.25, -0.25])


def test_update_preserves_current_entry_positions_after_root_is_moved() -> None:
    adapter = ManimLinearCombinationReadout(make_snapshot((0.0, 0.0), (0.0, 0.0)))
    adapter.shift(2.0 * RIGHT)
    entries = (*adapter.coefficient_entries, *adapter.result_entries)
    centers_before = tuple(entry.get_center().copy() for entry in entries)

    adapter.update_from_snapshot(make_snapshot((8.0, -12.5), (105.0, -0.125)))

    centers_after = tuple(entry.get_center() for entry in entries)
    for before, after in zip(centers_before, centers_after, strict=True):
        np.testing.assert_allclose(after, before)


def test_single_coefficient_and_higher_dimensional_result_are_supported() -> None:
    snapshot = LinearCombination([[1.0, 2.0, 3.0, 4.0]]).snapshot(-0.5)
    adapter = ManimLinearCombinationReadout(snapshot)

    assert adapter.vector_count == 1
    assert adapter.dimension == 4
    np.testing.assert_allclose(entry_values(adapter.coefficient_entries), [-0.5])
    np.testing.assert_allclose(
        entry_values(adapter.result_entries),
        [-0.5, -1.0, -1.5, -2.0],
    )


def test_changed_coefficient_count_is_rejected_before_any_entry_mutates() -> None:
    adapter = ManimLinearCombinationReadout(make_snapshot())
    old_coefficients = entry_values(adapter.coefficient_entries)
    old_result = entry_values(adapter.result_entries)

    with pytest.raises(ValueError, match="coefficient count changed"):
        adapter.update_from_snapshot(make_snapshot((1.0, 2.0, 3.0), (4.0, 5.0)))

    np.testing.assert_allclose(entry_values(adapter.coefficient_entries), old_coefficients)
    np.testing.assert_allclose(entry_values(adapter.result_entries), old_result)


def test_changed_result_dimension_is_rejected_before_any_entry_mutates() -> None:
    adapter = ManimLinearCombinationReadout(make_snapshot())
    old_coefficients = entry_values(adapter.coefficient_entries)
    old_result = entry_values(adapter.result_entries)

    with pytest.raises(ValueError, match="result dimension changed"):
        adapter.update_from_snapshot(make_snapshot((9.0, 8.0), (7.0, 6.0, 5.0)))

    np.testing.assert_allclose(entry_values(adapter.coefficient_entries), old_coefficients)
    np.testing.assert_allclose(entry_values(adapter.result_entries), old_result)


def test_missing_canonical_snapshot_fields_are_rejected() -> None:
    with pytest.raises(TypeError, match="coefficients and result"):
        ManimLinearCombinationReadout(object())


@pytest.mark.parametrize(
    "snapshot, message",
    [
        (ReadoutSnapshot(np.zeros((2, 1)), np.zeros(2)), "coefficients"),
        (ReadoutSnapshot(np.zeros(2), np.zeros((2, 1))), "result"),
        (ReadoutSnapshot(np.array([]), np.zeros(2)), "at least one"),
        (ReadoutSnapshot(np.zeros(2), np.array([])), "at least one"),
    ],
)
def test_invalid_shapes_and_empty_vectors_are_rejected(snapshot, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        ManimLinearCombinationReadout(snapshot)


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
def test_nonfinite_snapshot_values_are_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        ManimLinearCombinationReadout(
            ReadoutSnapshot(np.array([1.0, bad_value]), np.array([2.0, 3.0]))
        )
    with pytest.raises(ValueError, match="finite"):
        ManimLinearCombinationReadout(
            ReadoutSnapshot(np.array([1.0, 2.0]), np.array([3.0, bad_value]))
        )


@pytest.mark.parametrize("value", [-1, -3])
def test_negative_decimal_place_count_is_rejected(value: int) -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        ManimLinearCombinationReadout(make_snapshot(), num_decimal_places=value)


@pytest.mark.parametrize("value", [1.5, True, "2"])
def test_decimal_place_count_must_be_an_integer(value) -> None:
    with pytest.raises(TypeError, match="integer"):
        ManimLinearCombinationReadout(make_snapshot(), num_decimal_places=value)


@pytest.mark.parametrize(
    "argument, value, exception, message",
    [
        ("row_buff", -0.1, ValueError, "nonnegative"),
        ("block_buff", np.inf, ValueError, "finite"),
        ("row_buff", "wide", TypeError, "real scalar"),
    ],
)
def test_layout_buffer_validation(argument, value, exception, message) -> None:
    with pytest.raises(exception, match=message):
        ManimLinearCombinationReadout(make_snapshot(), **{argument: value})


def test_labels_must_be_nonempty_strings() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        ManimLinearCombinationReadout(make_snapshot(), coefficient_label="   ")
    with pytest.raises(TypeError, match="must be a string"):
        ManimLinearCombinationReadout(make_snapshot(), result_label=3)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "reserved_key",
    ["matrix", "element_to_mobject", "element_to_mobject_config"],
)
def test_matrix_style_cannot_override_adapter_owned_arguments(reserved_key: str) -> None:
    with pytest.raises(ValueError, match="adapter-owned"):
        ManimLinearCombinationReadout(
            make_snapshot(),
            matrix_kwargs={reserved_key: object()},
        )


def test_style_mappings_are_copied_without_mutating_inputs() -> None:
    label_kwargs = {"font_size": 31}
    matrix_kwargs = {"v_buff": 0.55, "h_buff": 0.8}

    ManimLinearCombinationReadout(
        make_snapshot(),
        label_kwargs=label_kwargs,
        matrix_kwargs=matrix_kwargs,
    )

    assert label_kwargs == {"font_size": 31}
    assert matrix_kwargs == {"v_buff": 0.55, "h_buff": 0.8}
