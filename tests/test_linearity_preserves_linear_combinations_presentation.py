import inspect

from scenes.linearity_preserves_linear_combinations_presentation import (
    LinearityPreservesLinearCombinationsPresentation,
)


def test_scene_compares_two_routes():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation
    )

    assert "_build_linear_combination" in source
    assert "_transform_combination" in source
    assert "_transform_components_separately" in source
    assert "_scale_and_add_transformed_components" in source


def test_transformed_combination_is_retained():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation._clear_first_construction
    )

    assert "FadeOut(original_group)" in source
    assert "FadeOut(combination_group)" in source
    assert "FadeOut(retained_result)" not in source



def test_subtitle_separates_latex_commands():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation.construct
    )

    assert r'r"\quad\text{versus}\quad",' in source
    assert r"\quadaT" not in source


def test_scene_states_full_linearity():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation
    )

    assert r"T(a\mathbf{u}+b\mathbf{v})" in source
    assert r"aT(\mathbf{u})+bT(\mathbf{v})" in source
    # The current revision states linearity symbolically rather than with
    # the earlier prose sentence.


def test_final_card_states_current_full_linearity_rule():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation._show_linearity_statement
    )

    assert r"T(a\mathbf{u}+b\mathbf{v})" in source
    assert r"aT(\mathbf{u})+bT(\mathbf{v})" in source


def test_matrix_card_shows_explicit_matrix_vector_product():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation._matrix_card
    )

    assert "matrix_tex" in source
    assert "input_vector" in source
    assert "matrix-vector multiplication" in source
    assert r"A\mathbf{x}" in source


def test_final_card_connects_matrix_multiplication_to_linearity():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation._show_linearity_statement
    )

    assert r"A(c\mathbf{v})=c(A\mathbf{v})" in source
    assert r"A(\mathbf{u}+\mathbf{v})" in source
    assert "Matrix multiplication preserves both scaling and addition." in source
    assert "Therefore every matrix transformation is linear." in source

def test_coordinate_plane_is_shifted_away_from_matrix_card():
    source = inspect.getsource(
        LinearityPreservesLinearCombinationsPresentation.construct
    )

    assert "x_length=8.1" in source
    assert "y_length=5.1" in source
    assert "LEFT * 0.42 + DOWN * 0.62" in source

