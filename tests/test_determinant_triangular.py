from engine.determinant_triangular import (
    block_example_factorization_tex,
    block_triangular_rule_tex,
    block_triangular_symbolic_tex,
    diagonal_product_tex,
    lower_triangular_determinant,
    lower_triangular_example,
    strategy_lines,
    triangular_explanation_lines,
    triangular_rule_tex,
    upper_triangular_determinant,
    upper_triangular_diagonal,
    upper_triangular_example,
)


def test_upper_triangular_example_and_diagonal() -> None:
    matrix = upper_triangular_example()
    assert matrix[1][0] == 0
    assert matrix[2][0:2] == (0, 0)
    assert matrix[3][0:3] == (0, 0, 0)
    assert upper_triangular_diagonal() == (2, -2, 3, 4)
    assert upper_triangular_determinant() == -48


def test_upper_triangular_formula_text() -> None:
    assert diagonal_product_tex() == r"\det(U)=2(-2)(3)(4)=-48"
    assert triangular_rule_tex() == r"\det(T)=t_{11}t_{22}\cdots t_{nn}"


def test_explanation_is_recursive() -> None:
    lines = triangular_explanation_lines()
    assert "zeros" in lines[0]
    assert "diagonal entry" in lines[1]
    assert "1x1 determinants" in lines[2]


def test_lower_triangular_example() -> None:
    matrix = lower_triangular_example()
    assert matrix[0][1:] == (0, 0)
    assert matrix[1][2] == 0
    assert lower_triangular_determinant() == -30


def test_block_triangular_rule() -> None:
    assert r"\begin{bmatrix}A&B\\0&D\end{bmatrix}" in block_triangular_symbolic_tex()
    assert block_triangular_rule_tex() == r"\det(M)=\det(A)\det(D)"
    assert "(8)(-3)=-24" in block_example_factorization_tex()


def test_strategy_lines_emphasize_structure() -> None:
    lines = strategy_lines()
    assert "look for structure" in lines[0]
    assert "multiply the diagonal entries" in lines[1]
    assert "multiply the block determinants" in lines[2]
