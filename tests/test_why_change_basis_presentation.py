from pathlib import Path


SCENE_PATH = Path("scenes/why_change_basis_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_lesson_identity_and_unnumbered_banner_are_present() -> None:
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "Why Change Basis?"' in text
    assert "CHAPTER 8" not in text


def test_same_vector_has_standard_and_basis_coordinates() -> None:
    text = source()
    assert r"[\mathbf v]_{\mathcal E}=\begin{bmatrix}4\\2\end{bmatrix}" in text
    assert r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}" in text
    assert r"\mathbf v=3\mathbf b_1+\mathbf b_2" in text


def test_basis_vectors_and_oblique_lattice_are_explicit() -> None:
    text = source()
    assert "def _oblique_lattice" in text
    assert r"\mathbf b_1" in text
    assert r"\mathbf b_2" in text
    assert "FadeOut(plane), FadeIn(lattice)" in text
    assert "A new basis is a new coordinate language for the same geometry." in text


def test_geometric_vector_is_created_once_and_not_transformed() -> None:
    text = source()
    assert text.count("vector = Arrow(") == 1
    assert "Transform(vector" not in text
    assert "ReplacementTransform(vector" not in text
    assert 'Text("The vector did not change."' in text
    assert 'Text("Only its coordinate"' in text
    assert 'Text("description changed."' in text


def test_complete_final_panel_is_constrained_to_safe_area() -> None:
    text = source()
    assert "final_panel = VGroup(comparison, takeaway).arrange" in text
    assert "final_panel.scale_to_fit_width(5.35)" in text
    assert "final_panel.scale_to_fit_height(4.55)" in text
    assert "final_panel.move_to(RIGHT * 3.15 + DOWN * 0.38)" in text


def test_math_uses_mathtex_and_student_scene_omits_checkpoint_number() -> None:
    text = source()
    assert "MathTex(" in text
    assert "CP187" not in text
