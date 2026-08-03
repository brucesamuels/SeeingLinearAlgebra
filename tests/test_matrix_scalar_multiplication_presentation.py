from pathlib import Path
S=Path("scenes/matrix_scalar_multiplication_presentation.py").read_text()
def test_scene(): assert "class MatrixScalarMultiplicationPresentation(Scene)" in S
def test_rule(): assert r"(cA)_{ij}=c\,a_{ij}" in S
def test_entries(): assert "scalar_entry_steps(" in S and "get_entries()" in S
def test_zero_negative(): assert "Negative and zero scalars" in S and r"0A=0" in S
def test_properties(): assert r"c(A+B)=cA+cB" in S and r"(c+d)A=cA+dA" in S and r"c(dA)=(cd)A" in S
def test_transform(): assert r"(cA)\mathbf{x}=c(A\mathbf{x})" in S
def test_pause_bridge(): assert "Pause and Predict" in S and "matrix–vector multiplication as a column combination" in S
