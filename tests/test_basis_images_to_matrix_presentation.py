import inspect

from scenes.basis_images_to_matrix_presentation import (
    BasisImagesToMatrixPresentation,
)


def test_coordinate_columns_are_read():
    source = inspect.getsource(
        BasisImagesToMatrixPresentation.read_coordinates
    )

    assert r"T(\mathbf e_1)=" in source
    assert r"T(\mathbf e_2)=" in source
    assert "DashedLine" in source


def test_columns_assemble_into_one_matrix():
    source = inspect.getsource(
        BasisImagesToMatrixPresentation.assemble_matrix
    )

    assert "assembled_matrix = Matrix(" in source
    assert "first_column.get_entries()" in source
    assert "second_column.get_entries()" in source
    assert "The transformed basis vectors become the columns." in source


def test_prediction_pause_is_present():
    source = inspect.getsource(
        BasisImagesToMatrixPresentation.construct
    )

    assert "Pause and Predict" in source
    assert "How should these two coordinate columns be organized?" in source


def test_clean_symbolic_screen_replaces_geometric_screen():
    source = inspect.getsource(
        BasisImagesToMatrixPresentation.explain_columns
    )

    assert "FadeOut(plane)" in source
    assert "FadeOut(images)" in source
    assert "FadeOut(coords)" in source
    assert "FadeOut(matrix_group)" in source
    assert "symbolic_screen = VGroup(" in source
    assert "Why these vectors become columns" in source
    assert "self.wait(4.0)" in source


def test_final_card_bridges_forward():
    source = inspect.getsource(
        BasisImagesToMatrixPresentation.final_card
    )

    assert (
        "The columns of a matrix are the images of the basis vectors."
        in source
    )
    assert "matrix-vector multiplication combines those columns." in source
