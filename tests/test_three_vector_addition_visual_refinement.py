from __future__ import annotations

import inspect

from scenes.three_vector_addition_presentation import ThreeVectorAdditionPresentation


def test_scene_uses_visibly_spread_vectors() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'assert snapshot.result == (4.0, 4.0, 5.0)' in source
    assert r'\mathbf{u}=(3,0,1)' in source
    assert r'\mathbf{v}=(0,3,1)' in source
    assert r'\mathbf{w}=(1,1,3)' in source


def test_sum_is_explicitly_named_as_body_diagonal() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'The sum is the body diagonal to the opposite corner.' in source
    assert 'Following u, then v, then w reaches the opposite corner.' in source
