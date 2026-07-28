from pathlib import Path

SCENE = Path("scenes/fundamental_subspaces_presentation.py")


def test_origin_is_imported_for_label_block_alignment() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "    ORIGIN," in source
    assert "aligned_edge=ORIGIN" in source


def test_input_and_output_labels_are_grouped_above_boxes() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'input_label_block = VGroup(input_title, input_subtitle).arrange(DOWN, buff=0.04, aligned_edge=ORIGIN).next_to(input_frame, UP, buff=0.22)' in source
    assert 'output_label_block = VGroup(output_title, output_subtitle).arrange(DOWN, buff=0.04, aligned_edge=ORIGIN).next_to(output_frame, UP, buff=0.22)' in source


def test_boxes_still_clear_later_text() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'FadeOut(input_frame), FadeOut(output_frame),' in source
    assert '.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(UP * 0.15)' in source
