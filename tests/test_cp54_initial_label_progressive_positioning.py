from __future__ import annotations

import inspect

from engine.manim_vector_to_origin_display import ManimVectorToOriginDisplay


def test_initial_label_uses_existing_progress_readout() -> None:
    source = inspect.getsource(
        ManimVectorToOriginDisplay._position_coordinate_labels
    )

    assert "progress = float(self._progress_number.get_value())" in source
    assert "progress = max(0.0, min(1.0, progress))" in source
    assert "_initial_tail_label_x" not in source


def test_initial_label_moves_progressively_left() -> None:
    source = inspect.getsource(
        ManimVectorToOriginDisplay._position_coordinate_labels
    )

    assert "base_right_shift = 0.22" in source
    assert "additional_left_travel = 0.95 * progress" in source
    assert "horizontal_shift = base_right_shift - additional_left_travel" in source
    assert "self.tail_label.shift(RIGHT * horizontal_shift)" in source


def test_initial_label_stays_close_to_the_tail() -> None:
    source = inspect.getsource(
        ManimVectorToOriginDisplay._position_coordinate_labels
    )

    assert "self.tail_label.next_to(self.tail_dot, DOWN, buff=0.12)" in source


def test_initial_label_clears_the_y_axis_at_all_progress_values() -> None:
    source = inspect.getsource(
        ManimVectorToOriginDisplay._position_coordinate_labels
    )

    assert "label_left = float(self.tail_label.get_left()[0])" in source
    assert "label_right = float(self.tail_label.get_right()[0])" in source
    assert "axis_margin = 0.12" in source
    assert (
        "if label_left - axis_margin <= axis_x <= "
        "label_right + axis_margin:" in source
    )
    assert "extra_left_shift = label_right - axis_x + axis_margin" in source
    assert "self.tail_label.shift(LEFT * extra_left_shift)" in source
