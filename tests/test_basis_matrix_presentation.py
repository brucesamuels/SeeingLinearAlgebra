from pathlib import Path


SCENE_PATH = Path("scenes/basis_matrix_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_lesson_identity_is_present_without_chapter_number() -> None:
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "The Basis Matrix"' in text
    assert "CHAPTER 8" not in text
    assert "CP189" not in text


def test_opening_card_states_the_coordinate_translation_problem() -> None:
    text = source()
    assert "What problem does the basis matrix solve?" in text
    assert "How do we translate a vector's coordinates" in text
    assert "from a nonstandard basis into the standard basis?" in text
    assert r"[\mathbf v]_{\mathcal B}" in text
    assert r"[\mathbf v]_{\mathcal E}" in text
    assert r"\xrightarrow{\qquad ?\qquad}" in text
    assert "Two coordinate columns describing the same vector" in text
    assert text.index("problem_card") < text.index("plane = NumberPlane")


def test_basis_matrix_is_built_from_basis_vector_columns() -> None:
    text = source()
    assert r"P_{\mathcal B}=[\,\mathbf b_1\ \mathbf b_2\,]" in text
    assert r"\begin{bmatrix}1&1\\1&-1\end{bmatrix}" in text
    assert "Each column is one geometric basis vector." in text


def test_matrix_multiplication_is_expanded_as_linear_combination() -> None:
    text = source()
    assert r"=3\begin{bmatrix}1\\1\end{bmatrix}" in text
    assert r"+1\begin{bmatrix}1\\-1\end{bmatrix}" in text
    assert r"=\begin{bmatrix}4\\2\end{bmatrix}" in text
    assert r"\boxed{\mathbf v=P_{\mathcal B}[\mathbf v]_{\mathcal B}}" in text


def test_decoder_examples_map_coordinate_units_to_basis_vectors() -> None:
    text = source()
    assert r"P_{\mathcal B}\begin{bmatrix}1\\0\end{bmatrix}=\mathbf b_1" in text
    assert r"P_{\mathcal B}\begin{bmatrix}0\\1\end{bmatrix}=\mathbf b_2" in text
    assert r"P_{\mathcal B}\begin{bmatrix}3\\1\end{bmatrix}=\mathbf v" in text


def test_graph_grid_is_pronounced_and_outputs_are_labeled() -> None:
    text = source()
    assert '"stroke_color": GREY_B, "stroke_width": 1.8, "stroke_opacity": 0.88' in text
    assert '"stroke_color": WHITE, "stroke_width": 3.0' in text
    assert r"[\mathbf b_1]_{\mathcal E}=(1,1)" in text
    assert r"[\mathbf b_2]_{\mathcal E}=(1,-1)" in text
    assert r"[\mathbf v]_{\mathcal E}=(4,2)" in text
    assert "ReplacementTransform(coordinate1, coordinate2)" in text
    assert "ReplacementTransform(coordinate2, coordinate3)" in text


def test_detailed_numerical_conversion_to_standard_basis_is_shown() -> None:
    text = source()
    assert r"[\mathbf u]_{\mathcal B}=\begin{bmatrix}2\\-1\end{bmatrix}" in text
    assert r"[\mathbf u]_{\mathcal E}" in text
    assert r"1(2)+1(-1)" in text
    assert r"1(2)+(-1)(-1)" in text
    assert r"\boxed{[\mathbf u]_{\mathcal E}=\begin{bmatrix}1\\3\end{bmatrix}}" in text


def test_reversed_order_display_has_been_removed() -> None:
    text = source()
    assert r"\mathbf b_2&\mathbf b_1" not in text
    assert "revers" not in text.lower()


def test_algebra_cards_use_large_math_and_safe_full_width() -> None:
    text = source()
    assert "font_size=63, color=YELLOW" in text
    assert "font_size=64, color=WHITE" in text
    assert "font_size=65, color=YELLOW" in text
    assert "group.scale_to_fit_width(11.2)" in text


def test_final_statement_names_standard_coordinates_explicitly() -> None:
    text = source()
    assert r"[\mathbf v]_{\mathcal E}=P_{\mathcal B}[\mathbf v]_{\mathcal B}" in text
    assert r"[\mathbf v]_{\mathcal E}=\mathbf v" in text
