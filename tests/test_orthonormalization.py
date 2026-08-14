import numpy as np
import pytest

from engine.orthonormalization import OrthonormalizationLesson


def test_snapshot_normalizes_orthogonal_pair() -> None:
    snapshot = OrthonormalizationLesson().snapshot()
    assert snapshot.norm_u1 == pytest.approx(np.sqrt(5.0))
    assert snapshot.norm_u2 == pytest.approx(np.sqrt(5.0))
    assert np.linalg.norm(snapshot.e1) == pytest.approx(1.0)
    assert np.linalg.norm(snapshot.e2) == pytest.approx(1.0)
    assert float(np.dot(snapshot.e1, snapshot.e2)) == pytest.approx(0.0)


def test_normalization_preserves_directions() -> None:
    snapshot = OrthonormalizationLesson().snapshot()
    assert np.allclose(snapshot.e1 * snapshot.norm_u1, snapshot.u1)
    assert np.allclose(snapshot.e2 * snapshot.norm_u2, snapshot.u2)


def test_lesson_statements_include_unit_orthogonal_span_and_qr_bridge() -> None:
    lesson = OrthonormalizationLesson()
    assert "=1" in lesson.UNIT_FACTS
    assert "cdot" in lesson.ORTHOGONALITY
    assert "span" in lesson.SPAN_FACT
    assert "columns of a matrix" in lesson.bridge_prompt
