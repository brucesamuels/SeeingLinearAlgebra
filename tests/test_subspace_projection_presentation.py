from pathlib import Path

SCENE_PATH = Path("scenes/subspace_projection_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_expected_banner_title_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Projection onto a Subspace"' in source
    assert 'SCENE_REVISION = "cp155_r4_card3_spacing_and_smoother_labels"' in source
    assert "class SubspaceProjectionPresentation(ThreeDScene)" in source


def test_scene_has_eight_cards() -> None:
    source = scene_source()
    for helper in (
        "_from_line_to_subspace_card",
        "_formula_analogy_card",
        "_derive_general_formula_card",
        "_general_basis_example_card",
        "_orthonormal_simplification_card",
        "_same_projection_card",
        "_residual_card",
        "_bridge_to_orthogonal_complement_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_world_labels_start_hidden_and_are_revealed_with_geometry() -> None:
    source = scene_source()
    assert "label.set_opacity(0)" in source
    assert "def _reveal" in source
    assert "self._reveal(x_label)" in source
    assert "self._reveal(p_label)" in source
    assert "self._reveal(r_label)" in source


def test_scene_explicitly_compares_line_and_general_subspace_formulas() -> None:
    source = scene_source()
    assert "self.lesson.LINE_FORMULA" in source
    assert "self.lesson.GENERAL_MATRIX_FORMULA" in source
    assert r"\frac{1}{\mathbf a^T\mathbf a}" in source
    assert r"(A^TA)^{-1}" in source
    assert "There is no matrix division" in source


def test_scene_derives_general_formula_from_orthogonal_residual() -> None:
    source = scene_source()
    assert r"A^T\mathbf r=\mathbf 0" in source
    assert r"A^T(\mathbf x-A\mathbf c)=\mathbf 0" in source
    assert "self.lesson.NORMAL_EQUATIONS" in source
    assert r"\mathbf c=(A^TA)^{-1}A^T\mathbf x" in source


def test_scene_computes_with_nonorthonormal_basis_matrix() -> None:
    source = scene_source()
    assert "The formula works for a non-orthonormal basis" in source
    assert r"A=\begin{bmatrix}1&1\\1&1\\0&2\end{bmatrix}" in source
    assert r"A^TA=\begin{bmatrix}2&2\\2&6\end{bmatrix}" in source
    assert r"(A^TA)^{-1}=\frac18\begin{bmatrix}6&-2\\-2&2\end{bmatrix}" in source
    assert r"\mathbf c=(A^TA)^{-1}A^T\mathbf x=\begin{bmatrix}1\\1\end{bmatrix}" in source
    assert r"\mathbf p=A\mathbf c=\begin{bmatrix}2\\2\\2\end{bmatrix}" in source


def test_scene_presents_orthonormal_formula_as_simplification() -> None:
    source = scene_source()
    assert "Orthonormal columns make the inverse disappear" in source
    assert r"Q^TQ=I" in source
    assert r"Q(Q^TQ)^{-1}Q^T\mathbf x" in source
    assert r"=QI Q^T\mathbf x=QQ^T\mathbf x" in source
    assert "self.lesson.ORTHONORMAL_SUM_FORMULA" in source


def test_scene_emphasizes_projection_is_basis_independent() -> None:
    source = scene_source()
    assert "The projection depends on W, not on the chosen basis" in source
    assert "self.lesson.GENERAL_PROJECTION_MATRIX" in source
    assert "self.lesson.PROJECTION_MATRIX" in source


def test_scene_residual_is_explicitly_orthogonal_to_W() -> None:
    source = scene_source()
    assert r"\mathbf r=\mathbf x-\mathbf p=(1,-1,0)" in source
    assert r"A^T\mathbf r=\mathbf 0" in source
    assert r"\mathbf r\perp W" in source


def test_scene_bridges_to_orthogonal_complement() -> None:
    source = scene_source()
    assert "Where do all vectors perpendicular to W live?" in source
    assert r"W^\perp" in source
    assert "orthogonal complement" in source.lower()


def test_scene_uses_slower_course_pacing() -> None:
    source = scene_source()
    assert "TRANSITION_TIME = 1.35" in source
    assert "EMPHASIS_TIME = 1.15" in source
    assert "LONG_HOLD_TIME = 3.0" in source

def test_card3_spacing_and_smoother_label_transitions() -> None:
    source = scene_source()
    assert "SCENE_REVISION = \"cp155_r4_card3_spacing_and_smoother_labels\"" in source
    assert "font_size=34," in source
    assert "move_to(UP * 1.45)" in source
    assert "arrange(DOWN, buff=0.30).move_to(DOWN * 0.58)" in source
    assert "return FadeIn(label)" in source
    assert "def _hide(label: MathTex):" in source
    assert "return FadeOut(label)" in source
