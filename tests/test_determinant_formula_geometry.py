import numpy as np
import pytest
from engine.determinant_formula_geometry import as_matrix_2x2, determinant, build_symbolic_derivation, final_statement

def test_validation():
    with pytest.raises(ValueError): as_matrix_2x2([[1,2,3],[4,5,6]])
    with pytest.raises(ValueError): as_matrix_2x2([[1,np.nan],[0,1]])

def test_determinant():
    assert determinant([[3,1],[1,2]]) == 5.0

def test_symbolic_derivation():
    d=build_symbolic_derivation()
    assert d.vertices == ("(0,0)","(a,c)","(a+b,c+d)","(b,d)")
    assert d.rectangle_area == "(a+b)(c+d)"
    assert d.outside_pieces == ("ac/2","bc","bd/2","bd/2","bc","ac/2")
    assert d.outside_total == "ac+bd+2bc"
    assert d.encasement_result.endswith("=ad-bc")
    assert d.shoelace_result.endswith("=ad-bc")

def test_final_statement():
    s=final_statement().lower(); assert "rectangle" in s and "shoelace" in s
