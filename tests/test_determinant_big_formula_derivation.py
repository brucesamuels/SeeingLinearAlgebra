from engine.determinant_big_formula_derivation import (
    all_selection_patterns,
    determinant_formula_tex,
    negative_patterns,
    negative_sum_tex,
    positive_patterns,
    positive_sum_tex,
    selection_pattern,
)


def test_all_six_selection_patterns_exist() -> None:
    patterns = all_selection_patterns()
    assert len(patterns) == 6
    assert {p.permutation for p in patterns} == {
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    }


def test_selection_coordinates_use_each_row_and_column_once() -> None:
    pattern = selection_pattern((2, 3, 1))
    assert pattern.coordinates == ((1, 2), (2, 3), (3, 1))
    assert pattern.product_tex == r"a_{12}a_{23}a_{31}"


def test_positive_negative_split() -> None:
    assert len(positive_patterns()) == 3
    assert len(negative_patterns()) == 3
    assert all(p.sign == 1 for p in positive_patterns())
    assert all(p.sign == -1 for p in negative_patterns())


def test_sum_formulas() -> None:
    assert r"a_{11}a_{22}a_{33}" in positive_sum_tex()
    assert r"a_{13}a_{21}a_{32}" in positive_sum_tex()
    assert r"a_{11}a_{23}a_{32}" in negative_sum_tex()
    assert determinant_formula_tex().startswith(r"\det(A)=")


def test_negative_sum_shows_negative_signs() -> None:
    assert negative_sum_tex().startswith(r"-a_{11}a_{23}a_{32}")
    assert r"-a_{12}a_{21}a_{33}" in negative_sum_tex()
    assert r"-a_{13}a_{22}a_{31}" in negative_sum_tex()
    assert r"+-" not in determinant_formula_tex()
