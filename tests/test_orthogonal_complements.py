import numpy as np
import pytest

from engine.orthogonal_complements import OrthogonalComplementsLesson


def test_residual_snapshot_has_expected_split_and_orthogonality() -> None:
    snapshot = OrthogonalComplementsLesson().residual_snapshot()
    assert np.allclose(snapshot.projection + snapshot.residual, snapshot.x)
    assert float(np.dot(snapshot.w_direction, snapshot.wp_direction)) == pytest.approx(0.0)
    assert float(np.dot(snapshot.projection, snapshot.residual)) == pytest.approx(0.0)


def test_plane_snapshot_has_plane_and_normal_data() -> None:
    snapshot = OrthogonalComplementsLesson().plane_snapshot()
    assert float(np.dot(snapshot.plane_basis_1, snapshot.complement_direction)) == pytest.approx(0.0)
    assert float(np.dot(snapshot.plane_basis_2, snapshot.complement_direction)) == pytest.approx(0.0)


def test_lesson_statements_capture_definition_and_decomposition() -> None:
    lesson = OrthogonalComplementsLesson()
    assert "W^\\perp" in lesson.DEFINITION
    assert lesson.DECOMPOSITION == r"\mathbb R^n=W\oplus W^\perp"
    assert lesson.DIMENSION_FACT == r"\dim W+\dim W^\perp=n"
    assert "orthogonal directions" in lesson.bridge_prompt
