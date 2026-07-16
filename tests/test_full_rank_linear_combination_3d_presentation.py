from __future__ import annotations
from pathlib import Path
import numpy as np
import pytest
pytest.importorskip("manim")
import scenes.full_rank_linear_combination_3d_presentation as presentation
from scenes.full_rank_linear_combination_3d_presentation import (
    FullRankLinearCombination3DPresentation,
    TARGET_COEFFICIENTS,
    _original_column_matrix,
    _result_for_coefficients,
    _scaled_column_matrix,
    _scaled_vectors,
)
from scenes.linear_combination_native_3d_smoke import SMOKE_VECTORS


def test_presentation_is_native_three_d() -> None:
    from manim import ThreeDScene
    assert issubclass(FullRankLinearCombination3DPresentation, ThreeDScene)


def test_original_matrix_contains_original_vectors_as_columns() -> None:
    np.testing.assert_allclose(_original_column_matrix(), SMOKE_VECTORS.T)


def test_scalars_update_original_columns_and_vectors() -> None:
    np.testing.assert_allclose(
        _scaled_column_matrix(TARGET_COEFFICIENTS),
        SMOKE_VECTORS.T * TARGET_COEFFICIENTS[np.newaxis, :],
    )
    np.testing.assert_allclose(
        _scaled_vectors(TARGET_COEFFICIENTS),
        TARGET_COEFFICIENTS[:, np.newaxis] * SMOKE_VECTORS,
    )


def test_result_is_sum_of_scaled_original_vectors() -> None:
    np.testing.assert_allclose(
        _result_for_coefficients(TARGET_COEFFICIENTS),
        _scaled_vectors(TARGET_COEFFICIENTS).sum(axis=0),
    )


def test_original_vectors_are_drawn_before_scalars_change() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")
    draw_play = source.index("draw_tracker.animate.set_value(1.0)")
    scalar_play = source.index("tracker.animate.set_value(float(target))")
    assert draw_play < scalar_play


def test_coefficient_trackers_begin_at_one_and_draw_trackers_at_zero() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")
    assert "coefficient_trackers = tuple(" in source
    assert "ValueTracker(1.0) for _ in range(3)" in source
    assert "draw_trackers = tuple(" in source
    assert "ValueTracker(0.0) for _ in range(3)" in source


def test_matrix_and_vectors_share_coefficient_trackers() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")
    assert "_scaled_column_matrix(current_coefficients())" in source
    assert "coefficient = coefficient_tracker.get_value()" in source
    assert "draw_progress * coefficient * vector" in source


def test_original_labels_transform_to_scaled_labels() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")
    assert "ReplacementTransform(old_label, new_label)" in source


def test_resultant_follows_scaling_and_half_turn_remains() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")
    assert source.index("tracker.animate.set_value(float(target))") < source.index(
        "final_result = _result_for_coefficients(TARGET_COEFFICIENTS)"
    )
    assert "theta=138 * DEGREES" in source


def test_camera_reframes_geometry_without_resizing_arrows() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")

    assert "CAMERA_ZOOM = 1.35" in source
    assert "zoom=CAMERA_ZOOM" in source

    # Preserve the established arrow, box, endpoint, and resultant dimensions.
    assert "thickness: float = 0.04" in source
    assert "0.25 * head_factor" in source
    assert "0.08 * head_factor" in source
    assert "thickness=0.007" in source
    assert "radius=0.075" in source
    assert "thickness=0.06" in source


def test_camera_zoom_does_not_change_mathematical_coordinates() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")

    assert "GEOMETRY_SCALE" not in source
    assert "axes.c2p(*vector)" in source
    assert "draw_progress * coefficient * vector" in source
    assert "_scaled_vectors(TARGET_COEFFICIENTS)" in source


def test_target_coefficients_make_scaling_visually_distinct() -> None:
    np.testing.assert_allclose(
        TARGET_COEFFICIENTS,
        np.array([1.80, 0.45, 1.60]),
    )
    assert TARGET_COEFFICIENTS[0] >= 1.5
    assert TARGET_COEFFICIENTS[1] <= 0.5
    assert TARGET_COEFFICIENTS[2] >= 1.5


def test_vectors_use_one_continuous_arrow_object_per_vector() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")

    assert "dynamic_arrows = VGroup(" in source
    assert "_dynamic_arrow(" in source
    assert "self.add(dynamic_arrows)" in source
    assert "self.remove(shaft)" not in source
    assert "original_arrows" not in source
    assert "scaled_arrows" not in source


def test_arrowheads_reveal_continuously_during_growth() -> None:
    from scenes.full_rank_linear_combination_3d_presentation import (
        HEAD_REVEAL_END,
        HEAD_REVEAL_START,
        _head_reveal_factor,
    )

    assert _head_reveal_factor(0.0) == 0.0
    assert _head_reveal_factor(HEAD_REVEAL_START) == 0.0
    assert 0.0 < _head_reveal_factor(0.30) < 1.0
    assert _head_reveal_factor(HEAD_REVEAL_END) == 1.0
    assert _head_reveal_factor(1.0) == 1.0


def test_same_arrows_survive_the_coefficient_sweep() -> None:
    source = Path(presentation.__file__).read_text(encoding="utf-8")

    draw_index = source.index("draw_tracker.animate.set_value(1.0)")
    scale_index = source.index("tracker.animate.set_value(float(target))")
    box_index = source.index("box_edges = tuple(")

    assert draw_index < scale_index < box_index
    assert source.count("dynamic_arrows = VGroup(") == 1
