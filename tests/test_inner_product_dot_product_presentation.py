import inspect
from scenes.inner_product_dot_product_presentation import InnerProductDotProductPresentation

def test_scene_begins_with_question_not_formula():
    source = inspect.getsource(InnerProductDotProductPresentation.construct)
    assert InnerProductDotProductPresentation.TITLE == 'Can Two Vectors Produce a Number?'
    assert 'What is this number measuring?' in source
    assert 'ValueTracker' in source
    assert 'always_redraw' in source

def test_scene_animates_positive_zero_and_negative_values():
    source = inspect.getsource(InnerProductDotProductPresentation.construct)
    assert r'\langle\mathbf{u},\mathbf{v}\rangle>0' in source
    assert r'\langle\mathbf{u},\mathbf{v}\rangle=0' in source
    assert r'\langle\mathbf{u},\mathbf{v}\rangle<0' in source
    assert 'acute' in source and 'right' in source and 'obtuse' in source

def test_coordinate_formula_is_revealed_after_exploration():
    source = inspect.getsource(InnerProductDotProductPresentation._show_coordinate_rule)
    assert r'\mathbf{u}\cdot\mathbf{v}' in source
    assert r'=u_1v_1+u_2v_2' in source
    assert r'3(2)+0(2)=6' in source

def test_geometric_formula_and_consequences_are_present():
    source = inspect.getsource(InnerProductDotProductPresentation._show_geometric_rule)
    assert r'\|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta' in source
    assert r'\mathbf{v}\cdot\mathbf{v}=\|\mathbf{v}\|^2' in source
    assert r'\mathbf{u}\perp\mathbf{v}' in source

def test_inner_product_is_introduced_as_broader_idea():
    source = inspect.getsource(InnerProductDotProductPresentation._show_inner_product_conclusion)
    assert 'The dot product is one example of an inner product.' in source
    assert 'An inner product turns geometric relationships into numbers.' in source
