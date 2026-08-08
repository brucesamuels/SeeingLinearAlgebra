from engine.determinant_adjugate_inverse import (
    adjugate_definition_tex,
    closing_lines,
    cofactor_signs,
    cramer_connection_tex,
    diagonal_entry_tex,
    example_adjugate,
    example_cofactor_matrix,
    example_determinant,
    example_inverse_formula_tex,
    example_matrix,
    example_product_tex,
    identity_tex,
    inverse_formula_tex,
    off_diagonal_entry_tex,
)


def test_checkerboard_sign_pattern_is_standard() -> None:
    assert cofactor_signs() == (("+", "-", "+"), ("-", "+", "-"), ("+", "-", "+"))


def test_core_identity_and_inverse_formula_tex() -> None:
    assert adjugate_definition_tex() == r"\operatorname{adj}(A)=C^T\quad\text{where }C=[C_{ij}]\text{ is the cofactor matrix}"
    assert identity_tex() == r"A\operatorname{adj}(A)=\det(A)I"
    assert inverse_formula_tex() == r"A^{-1}=\frac{1}{\det(A)}\operatorname{adj}(A)\quad\text{when }\det(A)\neq0"


def test_identity_explanations_reference_diagonal_and_off_diagonal_entries() -> None:
    assert "Diagonal entries" in diagonal_entry_tex()
    assert "cofactor expansions" in diagonal_entry_tex()
    assert "Off-diagonal entries" in off_diagonal_entry_tex()
    assert "equal rows" in off_diagonal_entry_tex()


def test_two_by_two_example_data_are_consistent() -> None:
    assert example_matrix() == ((2, 1), (5, 3))
    assert example_determinant() == 1
    assert example_cofactor_matrix() == ((3, -5), (-1, 2))
    assert example_adjugate() == ((3, -1), (-5, 2))


def test_two_by_two_formula_and_verification_tex() -> None:
    tex = example_inverse_formula_tex()
    assert r"\begin{bmatrix}2&1\\5&3\end{bmatrix}^{-1}" in tex
    assert r"\begin{bmatrix}3&-1\\-5&2\end{bmatrix}" in tex
    assert r"2\cdot3-1\cdot5" in tex
    product = example_product_tex()
    assert r"\begin{bmatrix}1&0\\0&1\end{bmatrix}" in product


def test_cramers_connection_and_closing_lines() -> None:
    lines = cramer_connection_tex()
    assert lines[0] == r"\mathbf x=A^{-1}\mathbf b"
    assert r"\operatorname{adj}(A)\mathbf b" in lines[1]
    assert "Cramer's Rule" in lines[2]
    closing = closing_lines()
    assert "adjugate" in closing[0]
    assert "det(A) I" in closing[1]
    assert "inverse formula" in closing[2]
