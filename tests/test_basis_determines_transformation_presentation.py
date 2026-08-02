import inspect
from scenes.basis_determines_transformation_presentation import BasisDeterminesTransformationPresentation

def test_basis_decomposition_is_shown():
    source=inspect.getsource(BasisDeterminesTransformationPresentation)
    assert r"\mathbf x=2\mathbf e_1+\mathbf e_2" in source

def test_basis_images_reconstruct_output():
    source=inspect.getsource(BasisDeterminesTransformationPresentation)
    assert r"T(\mathbf e_1)" in source
    assert r"T(\mathbf e_2)" in source
    assert r"2T(\mathbf e_1)+T(\mathbf e_2)" in source

def test_prediction_pause_is_present():
    source=inspect.getsource(BasisDeterminesTransformationPresentation.construct)
    assert "Pause and Predict" in source
    assert "Can T(x) be predicted" in source

def test_final_card_bridges_to_matrix_columns():
    source=inspect.getsource(BasisDeterminesTransformationPresentation.final_card)
    assert "completely determined by its action on a basis" in source
    assert "become the columns of a matrix" in source
