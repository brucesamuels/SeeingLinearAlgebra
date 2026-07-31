import inspect
from scenes.matrix_composition_presentation import MatrixCompositionPresentation

def test_scene_states_composition_identity():
    source = inspect.getsource(MatrixCompositionPresentation)
    assert r"A(B\mathbf{x})=(AB)\mathbf{x}" in source
    assert "B acts first. A acts second." in source
    assert "Multiplying matrices combines linear transformations." in source

def test_scene_contains_pause_and_predict():
    source = inspect.getsource(MatrixCompositionPresentation.construct)
    assert "Pause and Predict" in source
    assert "Will applying AB all at once land at the same point?" in source

def test_scene_compares_ab_and_ba():
    source = inspect.getsource(MatrixCompositionPresentation._show_conclusion)
    assert r"AB=" in source
    assert r"BA=" in source
    assert "In general, AB is not equal to BA." in source

def test_matrix_card_is_in_upper_right():
    source = inspect.getsource(MatrixCompositionPresentation._matrix_card)
    assert "to_corner(RIGHT + UP)" in source
