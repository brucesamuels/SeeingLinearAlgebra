from pathlib import Path
SCENE=Path('scenes/which_transformations_are_linear_presentation.py')
def test_scene_contains_required_tests():
    s=SCENE.read_text(); assert r'T(\mathbf{0})=\mathbf{0}' in s; assert r'T(c\mathbf{v})=cT(\mathbf{v})' in s; assert r'T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v})' in s
def test_scene_uses_examples():
    s=SCENE.read_text(); assert 'shear' in s and 'translation' in s and 'radial_nonlinear' in s
