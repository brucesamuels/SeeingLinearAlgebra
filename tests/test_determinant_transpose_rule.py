from engine.determinant_transpose_rule import (
    big_formula_tex,
    closing_lines,
    conclusion_tex,
    product_rewrite_tex,
    reindex_sum_tex,
    sign_invariance_tex,
    theorem_tex,
    transpose_formula_tex,
)


def test_theorem_tex_states_transpose_rule() -> None:
    assert theorem_tex() == r"\det(A^T)=\det(A)"


def test_big_formula_tex_uses_permutation_sum() -> None:
    text = big_formula_tex()
    assert r"\sum_{\sigma\in S_n}" in text
    assert r"\operatorname{sgn}(\sigma)" in text
    assert r"\prod_{i=1}^n a_{i,\sigma(i)}" in text


def test_transpose_formula_replaces_transpose_entries() -> None:
    first, second = transpose_formula_tex()
    assert r"(A^T)_{i,\sigma(i)}" in first
    assert r"a_{\sigma(i),i}" in second


def test_product_rewrite_introduces_inverse_permutation() -> None:
    formula, note = product_rewrite_tex()
    assert r"\sigma^{-1}(j)" in formula
    assert "Rename" in note


def test_reindex_sum_uses_tau_equals_sigma_inverse() -> None:
    first, second, third = reindex_sum_tex()
    assert r"\sigma^{-1}(j)" in first
    assert r"\tau=\sigma^{-1}" in second
    assert r"\operatorname{sgn}(\tau^{-1})" in third


def test_sign_invariance_and_conclusion_finish_the_proof() -> None:
    sign_formula, sign_note = sign_invariance_tex()
    assert r"\operatorname{sgn}(\tau^{-1})=\operatorname{sgn}(\tau)" == sign_formula
    assert "same parity" in sign_note
    first, second, third = conclusion_tex()
    assert r"\operatorname{sgn}(\tau)" in first
    assert second == r"=\det(A)"
    assert third == theorem_tex()


def test_closing_lines_emphasize_row_column_symmetry() -> None:
    lines = closing_lines()
    assert "rows and columns" in lines[0]
    assert "inverse permutation" in lines[1]
    assert "rows" in lines[2] and "columns" in lines[2]
