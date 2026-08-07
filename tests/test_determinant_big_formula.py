from engine.determinant_big_formula import (
    big_formula_explanation_lines,
    big_formula_tex,
    familiar_formula_3x3_tex,
    grouped_formula_3x3_lines,
    negative_terms_3x3,
    permutation_sign,
    permutation_terms_3x3,
    positive_terms_3x3,
)


def test_permutation_sign_detects_parity() -> None:
    assert permutation_sign((1, 2, 3)) == 1
    assert permutation_sign((1, 3, 2)) == -1
    assert permutation_sign((2, 3, 1)) == 1
    assert permutation_sign((3, 2, 1)) == -1


def test_three_by_three_has_six_terms() -> None:
    terms = permutation_terms_3x3()
    assert len(terms) == 6
    assert {term.permutation for term in terms} == {
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    }


def test_positive_and_negative_terms_split_evenly() -> None:
    positives = positive_terms_3x3()
    negatives = negative_terms_3x3()
    assert len(positives) == 3
    assert len(negatives) == 3
    assert all(term.sign == 1 for term in positives)
    assert all(term.sign == -1 for term in negatives)


def test_formula_strings_exist() -> None:
    assert r"\sum_{\sigma\in S_n}" in big_formula_tex()
    assert r"\operatorname{sgn}(\sigma)" in big_formula_tex()
    assert r"a_{11}a_{22}a_{33}" in familiar_formula_3x3_tex()
    assert r"a_{13}a_{22}a_{31}" in familiar_formula_3x3_tex()


def test_grouped_lines_and_explanations() -> None:
    positive, negative = grouped_formula_3x3_lines()
    assert r"\text{positive: }" in positive
    assert r"\text{negative: }" in negative
    explanations = big_formula_explanation_lines()
    assert explanations[0] == "Pick exactly one entry from each row."
    assert explanations[1] == "Pick exactly one entry from each column."


def test_explanation_line_wraps_sign_statement() -> None:
    explanations = big_formula_explanation_lines()
    assert 'even permutations' in explanations[3]
    assert '\n' in explanations[3]
