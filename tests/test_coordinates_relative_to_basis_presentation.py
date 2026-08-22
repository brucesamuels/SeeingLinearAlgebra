from pathlib import Path


SCENE_PATH = Path("scenes/coordinates_relative_to_basis_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_lesson_identity_is_present_without_chapter_number() -> None:
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "Coordinates Relative to a Basis"' in text
    assert "CHAPTER 8" not in text
    assert "CP188" not in text


def test_geometry_builds_three_b1_plus_b2_tip_to_tail() -> None:
    text = source()
    assert "step1 = Arrow(p0, p1" in text
    assert "step2 = Arrow(p1, p2" in text
    assert "step3 = Arrow(p2, p3" in text
    assert "step4 = Arrow(p3, p4" in text
    assert r"\mathbf v=3\mathbf b_1+1\mathbf b_2" in text


def test_coordinate_column_and_correspondence_are_explicit() -> None:
    text = source()
    assert r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}" in text
    assert r"3\longleftrightarrow\mathbf b_1" in text
    assert r"1\longleftrightarrow\mathbf b_2" in text


def test_coordinate_column_is_distinguished_from_geometric_vector() -> None:
    text = source()
    assert 'Text("Geometric vector"' in text
    assert 'Text("B-coordinate description"' in text
    assert "not the geometric vector itself" in text
    assert r'MathTex(r"\mathbf v=\begin{bmatrix}4\\2\end{bmatrix}", font_size=56' in text
    assert r'MathTex(r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}", font_size=56' in text


def test_ordered_basis_reverses_coordinate_order() -> None:
    text = source()
    assert r"\mathcal B'=(\mathbf b_2,\mathbf b_1)" in text
    assert r"[\mathbf v]_{\mathcal B'}=\begin{bmatrix}1\\3\end{bmatrix}" in text
    assert r'MathTex(r"\mathcal B=(\mathbf b_1,\mathbf b_2)", font_size=54' in text
    assert "MathTex(r\"\\mathcal B'=(\\mathbf b_2,\\mathbf b_1)\", font_size=54" in text
    assert "font_size=54, color=BLUE_C" in text
    assert 'Text("Same vector; different ordering.", font_size=30' in text
    assert 'Text("Different coordinate column.", font_size=30' in text


def test_card_five_uses_full_width_without_height_downscaling() -> None:
    text = source()
    assert "FadeOut(plane), FadeOut(vector), FadeOut(vector_label)" in text
    assert "basis_comparison = VGroup(original, reversed_basis).arrange(RIGHT" in text
    assert "order_panel.scale_to_fit_width(11.2)" in text
    assert "order_panel.scale_to_fit_height" not in text
    assert "order_panel = self._fit_right" not in text


def test_all_right_panels_use_safe_area_fitting() -> None:
    text = source()
    assert "def _fit_right" in text
    assert "group.scale_to_fit_width(5.35)" in text
    assert "group.scale_to_fit_height(4.65)" in text
