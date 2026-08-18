from pathlib import Path

SCENE_PATH = Path("scenes/eigenvector_special_directions_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_clear_coordinate_grid_and_fixed_2d_scene() -> None:
    text = source()
    assert "class EigenvectorSpecialDirectionsPresentation(Scene):" in text
    assert "NumberPlane(" in text
    assert "ThreeDScene" not in text


def test_scene_first_animates_quarter_turn_then_contrasting_transformation() -> None:
    text = source()
    assert "ROTATION_MATRIX" in text
    assert r'R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}' in text
    assert r'A=\begin{bmatrix}5&3\\3&5\end{bmatrix}' in text
    assert "ReplacementTransform(rotation_tex, special_tex)" in text
    first_rotation = text.index("rotation_observations")
    later_special = text.index("special_observations")
    assert first_rotation < later_special


def test_scene_explicitly_states_rotation_has_no_same_line_direction() -> None:
    text = source()
    assert 'ROTATION_HEADING = "A 90° rotation moves every nonzero vector to a different line."' in text
    assert '"No image stays on its original line."' in text
    assert 'CONTRAST_HEADING = "Now compare a transformation with two special directions."' in text


def test_scene_resets_same_vectors_before_second_transformation() -> None:
    text = source()
    assert "for arrow, vector in zip(arrows, SAMPLE_VECTORS)" in text
    assert "arrow.animate.put_start_and_end_on(origin, plane.c2p(*vector))" in text
    assert '"Watch the original dashed lines again."' in text


def test_scene_delays_eigenvector_language_until_final_discovery() -> None:
    text = source()
    opening = text.index('OPENING_HEADING = "Do any directions stay on their original lines?"')
    final = text.index('FINAL_STATEMENT = "These special directions are eigenvector directions."')
    assert opening < final
    assert "A\\mathbf{v}=\\lambda\\mathbf{v}" not in text
    assert "characteristic" not in text.lower()


def test_scene_highlights_exactly_two_special_directions_in_second_act() -> None:
    text = source()
    assert "SPECIAL_INDICES = (4, 5)" in text
    assert 'SPECIAL_HEADING = "This time, two directions stay on the same line."' in text
    assert text.count('Text("same line"') == 2
    assert "set_color(YELLOW).set_opacity(0.90)" in text


def test_scene_retains_frozen_faded_dashed_ghost_arrows_for_original_vectors() -> None:
    text = source()
    assert "ghost_arrows = VGroup()" in text
    assert "ghost_arrow = DashedLine(" in text
    assert "color=self.VECTOR_COLORS[index]" in text
    assert "stroke_opacity=0.34" in text
    assert "FadeIn(ghost_arrows)" in text
    assert "special_display_scale = 0.48" in text
    # Ghost arrows are displayed as fixed references and are never transformed.
    ghost_block = text[text.index("ghost_arrows = VGroup()") : text.index("self.play(FadeIn(banner)") ]
    assert ".animate" not in ghost_block


def test_scene_holds_full_comparison_then_fades_generic_vectors_and_ghosts() -> None:
    text = source()
    assert "# Hold the full comparison" in text
    assert "self.wait(2.0)" in text
    assert "FadeOut(arrows[i]) for i in generic_indices" in text
    assert "FadeOut(ghost_arrows[i]) for i in generic_indices" in text
    assert "FadeOut(rays[i]) for i in generic_indices" in text


def test_student_facing_scene_contains_no_checkpoint_number() -> None:
    assert "CP168" not in source()
