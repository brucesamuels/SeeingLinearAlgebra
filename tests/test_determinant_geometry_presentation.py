from pathlib import Path

SCENE = Path("scenes/determinant_geometry_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_and_card_sequence_exist() -> None:
    text = source()
    assert "class DeterminantGeometryPresentation(Scene):" in text
    for call in (
        "self.show_unit_square_map(banner)",
        "self.show_area_scale(banner)",
        "self.show_orientation(banner)",
        "self.show_singular_collapse(banner)",
        "self.show_volume_scale(banner)",
        "self.show_volume_collapse(banner)",
        "self.show_multiplicativity_geometry(banner)",
        "self.show_takeaway(banner)",
    ):
        assert call in text


def test_scene_uses_visual_geometry_not_dense_proof_cards() -> None:
    text = source()
    assert "NumberPlane" in text
    assert "Polygon" in text
    assert "projected_box" in text
    assert "ReplacementTransform" in text


def test_scene_explains_area_orientation_and_collapse() -> None:
    text = source()
    assert "The determinant measures area scaling" in text
    assert "The sign records orientation" in text
    assert "orientation preserved" in text
    assert "orientation reversed" in text
    assert "If det(A)=0, area collapses" in text


def test_scene_extends_to_volume_and_product_rule() -> None:
    text = source()
    assert "In 3D, determinant magnitude scales volume" in text
    assert "A singular 3D map flattens volume" in text
    assert "Successive volume scalings multiply" in text
    assert "geometric meaning of det(AB)=det(A)det(B)" in text


def test_takeaway_reserves_large_formula_for_final_card() -> None:
    text = source()
    assert 'title = self.stage_title("The big takeaway", size=29)' in text
    assert 'MathTex(signed_scale_tex(), font_size=43, color=GREEN)' in text


def test_scene_uses_fixed_title_band_and_safe_clear_pattern() -> None:
    text = source()
    assert 'title.move_to(np.array([0.0, 2.28, 0.0]))' in text
    assert '*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]' in text
    assert 'VGroup(*self.mobjects)' not in text
