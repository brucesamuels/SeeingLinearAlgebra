import numpy as np
import pytest

from engine.gram_schmidt_two_vectors import GramSchmidtTwoVectorsLesson


def test_pair_snapshot_has_clean_projection_split() -> None:
    snapshot = GramSchmidtTwoVectorsLesson().pair_snapshot()
    assert np.allclose(snapshot.v2, snapshot.projection + snapshot.u2)
    assert np.allclose(snapshot.u1, snapshot.v1)
    assert float(np.dot(snapshot.u1, snapshot.u2)) == pytest.approx(0.0)


def test_projection_is_parallel_to_u1() -> None:
    snapshot = GramSchmidtTwoVectorsLesson().pair_snapshot()
    scale = snapshot.projection[0] / snapshot.u1[0]
    assert np.allclose(snapshot.projection, scale * snapshot.u1)
    assert scale == pytest.approx(2.0)


def test_lesson_statements_capture_formula_and_bridge() -> None:
    lesson = GramSchmidtTwoVectorsLesson()
    assert "proj" in lesson.STEP_FORMULA
    assert "span" in lesson.SPAN_FACT
    assert "orthonormal" in lesson.bridge_prompt
