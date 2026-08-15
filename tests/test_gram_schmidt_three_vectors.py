import numpy as np
import pytest

from engine.gram_schmidt_three_vectors import GramSchmidtThreeVectorsLesson


def test_snapshot_builds_clean_three_vector_example() -> None:
    snapshot = GramSchmidtThreeVectorsLesson().snapshot()
    assert np.allclose(snapshot.v2, snapshot.proj_v2_on_u1 + snapshot.u2)
    assert np.allclose(snapshot.v3, snapshot.proj_v3_on_u1 + snapshot.proj_v3_on_u2 + snapshot.u3)
    assert np.allclose(snapshot.w3, snapshot.v3 - snapshot.proj_v3_on_u1)


def test_orthogonal_vectors_are_pairwise_perpendicular() -> None:
    snapshot = GramSchmidtThreeVectorsLesson().snapshot()
    assert float(np.dot(snapshot.u1, snapshot.u2)) == pytest.approx(0.0)
    assert float(np.dot(snapshot.u1, snapshot.u3)) == pytest.approx(0.0)
    assert float(np.dot(snapshot.u2, snapshot.u3)) == pytest.approx(0.0)


def test_general_step_and_closing_prompt_are_present() -> None:
    lesson = GramSchmidtThreeVectorsLesson()
    assert "sum" in lesson.GENERAL_STEP
    assert "orthonormal" in lesson.NORMALIZE_NOTE
    assert "normalize" in lesson.closing_prompt
