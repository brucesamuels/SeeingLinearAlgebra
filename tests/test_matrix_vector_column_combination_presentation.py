import inspect
from scenes.matrix_vector_column_combination_presentation import MatrixVectorColumnCombinationPresentation

def test_symbolic_product_is_shown():
    source = inspect.getsource(MatrixVectorColumnCombinationPresentation.show_symbolic_product)
    assert r"A\mathbf x=" in source
    assert "matrix.get_entries()" in source
    assert "vector.get_entries()" in source

def test_column_combination_is_revealed():
    source = inspect.getsource(MatrixVectorColumnCombinationPresentation.reveal_column_combination)
    assert r"\begin{bmatrix}1\\2\end{bmatrix}" in source
    assert r"\begin{bmatrix}-1\\1\end{bmatrix}" in source
    assert "The vector entries become coefficients." in source

def test_prediction_pause_is_present():
    source = inspect.getsource(MatrixVectorColumnCombinationPresentation.construct)
    assert "Pause and Predict" in source
    assert "What role do the entries 2 and 1 play?" in source

def test_geometry_matches_column_combination():
    source = inspect.getsource(MatrixVectorColumnCombinationPresentation.show_geometric_combination)
    assert r"2\mathbf a_1" in source
    assert r"1\mathbf a_2" in source
    assert "The column combination lands exactly at Ax." in source

def test_final_card_bridges_forward():
    source = inspect.getsource(MatrixVectorColumnCombinationPresentation.show_conclusion)
    assert "Matrix–vector multiplication is a column combination" in source
    assert "row–column rule computes the same result entry by entry." in source
