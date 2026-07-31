import inspect

from scenes.cross_product_presentation import CrossProductPresentation


def test_scene_begins_with_geometric_question():
    source = inspect.getsource(CrossProductPresentation.construct)

    assert CrossProductPresentation.TITLE == (
        "What Can Two Vectors Produce in 3D?"
    )
    assert "What vector could describe both at once?" in source


def test_scene_shows_parallelogram_area():
    source = inspect.getsource(CrossProductPresentation.construct)

    assert "Parallelogram area" in source
    assert r"\|\mathbf{u}\times\mathbf{v}\|" in source
    assert "Its length is the area of the parallelogram." in source


def test_scene_rotates_camera_to_show_perpendicularity():
    source = inspect.getsource(CrossProductPresentation.construct)

    assert "Perpendicular to both vectors" in source
    assert "begin_ambient_camera_rotation" in source
    assert "stop_ambient_camera_rotation" in source


def test_scene_shows_anti_commutativity():
    source = inspect.getsource(CrossProductPresentation.construct)

    assert "Order matters" in source
    assert r"\mathbf{v}\times\mathbf{u}" in source
    assert r"-(\mathbf{u}\times\mathbf{v})" in source


def test_scene_concludes_with_oriented_area():
    source = inspect.getsource(CrossProductPresentation._show_conclusion)

    assert "Direction: perpendicular to both input vectors" in source
    assert "Magnitude: area of the spanned parallelogram" in source
    assert "Orientation: reversing the order reverses the vector" in source
    assert "The cross product measures oriented area." in source
