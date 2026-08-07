from engine.determinant_cofactor_efficiency import (
    arithmetic_lines,
    comparison_counts,
    determinant_2x2,
    determinant_value,
    example_matrix,
    first_expansion_step,
    first_expansion_tex,
    minor_3x3_value,
    recursive_expansion_tex,
    second_expansion_other_minor,
    second_expansion_step,
    strategy_lines,
)


def test_example_matrix_has_favorable_second_row() -> None:
    matrix = example_matrix()
    assert matrix[1] == (0, 3, 0, 0)
    assert matrix[1].count(0) == 3


def test_first_expansion_step() -> None:
    step = first_expansion_step()
    assert (step.row, step.column, step.entry, step.sign) == (2, 2, 3, 1)
    assert step.minor == ((2, 1, 0), (1, 2, 1), (0, 1, 2))


def test_recursive_minor_and_values() -> None:
    step = second_expansion_step()
    assert step.minor == ((2, 1), (1, 2))
    assert determinant_2x2(step.minor) == 3
    assert determinant_2x2(second_expansion_other_minor()) == 2
    assert minor_3x3_value() == 4
    assert determinant_value() == 12


def test_display_equations() -> None:
    assert r"\det(A)=3\det" in first_expansion_tex()
    assert r"2\begin{vmatrix}2&1\\1&2\end{vmatrix}" in recursive_expansion_tex()
    assert arithmetic_lines()[-1] == r"\det(A)=12"


def test_strategy_emphasizes_zeros() -> None:
    lines = strategy_lines()
    assert "any row or column" in lines[0]
    assert "Zeros" in lines[1]
    assert "as many zeros as possible" in lines[2]
    assert comparison_counts() == (1, 2)
