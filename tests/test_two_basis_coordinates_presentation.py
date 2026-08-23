from pathlib import Path

SCENE = Path("scenes/two_basis_coordinates_presentation.py")


def source(): return SCENE.read_text(encoding="utf-8")


def test_identity_and_opening_problem():
    text = source()
    assert 'CHAPTER_BANNER = "CHANGE OF BASIS"' in text
    assert 'LESSON_TITLE = "Changing Between Two Nonstandard Bases"' in text
    assert r"[\mathbf v]_{\mathcal B}\xrightarrow{\qquad ?\qquad}[\mathbf v]_{\mathcal C}" in text
    assert "CP191" not in text


def test_fixed_vector_and_explicit_grid_motion():
    text = source()
    assert text.count("vector = Arrow") == 1
    assert "Transform(grid_b, grid_c, rate_func=smooth)" in text
    assert "run_time=4.0" in text
    assert "ReplacementTransform(vector" not in text
    assert r"[\mathbf v]_{\mathcal B}=(3,1)" in text
    assert r"[\mathbf v]_{\mathcal C}=(2,1)" in text


def test_direction_and_numerical_example():
    text = source()
    assert r"T_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}" in text
    assert r"\boxed{[\mathbf v]_{\mathcal C}=P_{\mathcal C}^{-1}P_{\mathcal B}[\mathbf v]_{\mathcal B}}" in text
    assert 'Matrix([["1", "-1"], ["0", "1"]])' in text
    assert 'Matrix([["3-1"], ["1"]])' in text
    assert r"2(1,1)+1(2,0)=(4,2)=\mathbf v" in text


def test_matrix_cards_do_not_use_raw_bmatrix_rows():
    text = source()
    assert r"\begin{bmatrix}" not in text
    assert text.count(r'[["0", "1"], [r"\tfrac{1}{2}", r"-\tfrac{1}{2}"]]') == 2
    assert text.count("v_buff=1.15") == 2
    assert r"\frac12" not in text
