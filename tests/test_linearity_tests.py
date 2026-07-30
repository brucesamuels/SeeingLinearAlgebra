import numpy as np
from engine.linearity_tests import evaluate_linearity, radial_nonlinear, shear, translation
def test_shear_passes():
    s=evaluate_linearity("Shear",shear); assert s.fixes_origin and s.preserves_homogeneity and s.preserves_additivity and s.is_linear_on_tests
def test_translation_fails():
    s=evaluate_linearity("Translation",translation); assert not s.fixes_origin and not s.preserves_homogeneity and not s.preserves_additivity
def test_radial_fixes_origin_but_is_not_linear():
    s=evaluate_linearity("Radial",radial_nonlinear); assert s.fixes_origin and not s.preserves_homogeneity and not s.is_linear_on_tests
def test_shear_formula(): assert np.allclose(shear((2,3),factor=.5),(3.5,3))
