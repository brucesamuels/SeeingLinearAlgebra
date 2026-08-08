from engine.determinant_cramers_rule import (
    closing_lines,
    coefficient_matrix,
    column_equation_tex,
    derivation_lines_tex,
    determinant_a,
    example_ratios_tex,
    replacement_definition_tex,
    replacement_determinants,
    replacement_matrices,
    right_hand_side,
    solution_vector,
    theorem_condition_tex,
    theorem_tex,
)


def determinant3(M: tuple[tuple[int, ...], ...]) -> int:
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def test_example_system_has_expected_solution() -> None:
    A = coefficient_matrix()
    x = solution_vector()
    b = right_hand_side()
    product = tuple(sum(A[i][j] * x[j] for j in range(3)) for i in range(3))
    assert product == b


def test_base_determinant_is_nonzero() -> None:
    assert determinant3(coefficient_matrix()) == determinant_a() == 5


def test_replacement_determinants_are_correct() -> None:
    assert tuple(determinant3(M) for M in replacement_matrices()) == replacement_determinants()
    assert replacement_determinants() == (10, -5, 15)


def test_cramers_rule_recovers_solution() -> None:
    detA = determinant_a()
    recovered = tuple(det / detA for det in replacement_determinants())
    assert recovered == solution_vector()


def test_column_equation_and_replacement_definition() -> None:
    assert r"x_1\mathbf a_1" in column_equation_tex()
    assert r"\mathbf b" in replacement_definition_tex()
    assert r"A_k" in replacement_definition_tex()


def test_derivation_uses_linearity_and_isolates_xk() -> None:
    lines = derivation_lines_tex()
    assert r"\det(A_k)" in lines[0]
    assert r"\sum_{j=1}^{n}x_j\mathbf a_j" in lines[1]
    assert lines[2] == r"=x_k\det(A)"


def test_theorem_requires_nonzero_determinant() -> None:
    assert theorem_condition_tex() == r"\det(A)\neq0"
    assert theorem_tex() == r"x_k=\frac{\det(A_k)}{\det(A)},\qquad k=1,\ldots,n"


def test_example_ratios_show_final_solution() -> None:
    lines = example_ratios_tex()
    assert lines[0].endswith("=2")
    assert lines[1].endswith("=-1")
    assert lines[2].endswith("=3")


def test_closing_lines_note_scope_and_efficiency() -> None:
    joined = " ".join(closing_lines())
    assert "square" in joined
    assert "det(A) is nonzero" in joined
    assert "elimination" in joined
