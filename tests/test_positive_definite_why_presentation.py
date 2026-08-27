from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "positive_definite_why_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_has_live_direction_and_energy_readout():
    assert "ValueTracker" in TEXT
    assert "always_redraw" in TEXT
    assert "model.directional_energy(theta.get_value())" in TEXT
    assert "DecimalNumber" in TEXT


def test_scene_contains_sweep_pause_and_final_definition():
    assert "for target in" in TEXT
    assert "Can any nonzero direction make this value zero or negative?" in TEXT
    assert "Pause and predict." in TEXT
    assert r"x^T A x>0\quad\text{for every }x\ne 0" in TEXT
    assert "positive definite" in TEXT


def test_scene_stays_within_approved_scope():
    forbidden = ("eigenvalue", "pivot", "minor", "LDL", "Cholesky", "bowl")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)
    assert "CP199" not in TEXT
