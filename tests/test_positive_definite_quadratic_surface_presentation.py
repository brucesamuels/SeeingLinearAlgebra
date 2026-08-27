from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_quadratic_surface_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_connects_unit_directions_to_all_nonzero_vectors():
    assert r"x=ru,\qquad r>0,\qquad \lVert u\rVert=1" in TEXT
    assert r"q(ru)=(ru)^T A(ru)=r^2q(u)" in TEXT
    assert "radial_energy(radius.get_value(), theta)" in TEXT


def test_scene_builds_quadratic_surface_and_reference_plane():
    assert "class PositiveDefiniteQuadraticSurfacePresentation(ThreeDScene)" in TEXT
    assert "reference_plane = Surface(" in TEXT
    assert "surface = Surface(" in TEXT
    assert "model.surface_point(u, v)" in TEXT
    assert "begin_ambient_camera_rotation" in TEXT


def test_scene_contains_prediction_and_geometric_definition():
    assert "What would zero or negative quadratic energy look like here?" in TEXT
    assert "Pause and predict." in TEXT
    assert "zero_surface = Surface(" in TEXT
    assert r"z=3x^2" in TEXT
    assert "saddle_surface = Surface(" in TEXT
    assert r"z=3x^2-3y^2" in TEXT
    assert "Transform(surface, zero_surface)" in TEXT
    assert "Transform(surface, saddle_surface)" in TEXT
    assert "Transform(surface, restored_surface)" in TEXT
    assert "touches the plane only at the origin and never passes below it" in TEXT
    assert r"x^T A x>0\quad\text{for every }x\ne0" in TEXT
    assert "positive definite" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("eigenvalue", "pivot", "minor", "LDL", "Cholesky")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP200" not in TEXT
