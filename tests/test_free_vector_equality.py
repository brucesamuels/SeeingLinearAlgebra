from __future__ import annotations

import numpy as np
import pytest

from engine.free_vector_equality import FreeVectorEquality


def test_translated_copies_preserve_free_vector_identity() -> None:
    snapshot = FreeVectorEquality(
        [2.0, 1.0],
        origins=([0.0, 0.0], [3.0, -1.0], [-2.0, 4.0]),
    ).snapshot()

    assert snapshot.copy_count == 3
    assert snapshot.all_equal_as_free_vectors
    assert snapshot.distinct_origins

    for copy in snapshot.copies:
        np.testing.assert_allclose(copy.coordinates, [2.0, 1.0])
        np.testing.assert_allclose(copy.endpoint, copy.origin + copy.coordinates)
        assert copy.magnitude == pytest.approx(np.sqrt(5.0))


def test_snapshot_rejects_missing_origins() -> None:
    with pytest.raises(ValueError, match="at least one"):
        FreeVectorEquality([1.0, 2.0], origins=())


def test_origin_dimension_must_match_vector_dimension() -> None:
    with pytest.raises(ValueError, match="dimension"):
        FreeVectorEquality([1.0, 2.0], origins=([0.0, 0.0, 0.0],))
