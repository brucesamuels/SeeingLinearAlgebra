import inspect

import numpy as np
import pytest

from engine.svd_chapter_synthesis import SVDChapterSynthesis


def test_numerical_anchor_has_expected_singular_values_rank_and_condition_number():
    model = SVDChapterSynthesis()
    assert model.matrix.shape == (3, 2)
    assert np.allclose(model.singular_values(), [3, 0.5])
    assert model.rank() == 2
    assert model.condition_number() == pytest.approx(6)


def test_pseudoinverse_reverses_the_positive_stretches():
    model = SVDChapterSynthesis()
    assert np.allclose(model.pseudoinverse(), [[1 / 3, 0, 0], [0, 2, 0]])
    assert np.allclose(model.pseudoinverse() @ model.matrix, np.eye(2))


def test_rank_one_approximation_and_error_match_discarded_value():
    model = SVDChapterSynthesis()
    assert np.allclose(model.rank_one_approximation(), [[3, 0], [0, 0], [0, 0]])
    assert model.rank_one_error() == pytest.approx(0.5)
    assert model.rank_one_retained_energy() == pytest.approx(9 / 9.25)


def test_topics_cover_the_chapter_conceptual_arc():
    topics = SVDChapterSynthesis().topics()
    assert [topic.title for topic in topics] == [
        "Geometric structure",
        "Rank and subspaces",
        "Pseudoinverse",
        "Conditioning",
        "Approximation",
        "Image compression",
        "PCA",
        "Recognition",
    ]
    assert all(topic.question and topic.takeaway for topic in topics)


def test_recognition_rules_distinguish_four_uses_of_singular_values():
    rules = SVDChapterSynthesis().recognition_rules()
    assert [rule.operation for rule in rules] == [
        "Inverse",
        "Pseudoinverse",
        "Truncated SVD",
        "PCA",
    ]
    assert "every singular value" in rules[0].singular_value_action
    assert "leave zeros" in rules[1].singular_value_action
    assert "largest k" in rules[2].singular_value_action
    assert "center data" in rules[3].singular_value_action


def test_engine_composes_truncated_svd_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(SVDChapterSynthesis))
    assert "from engine.truncated_svd_approximation import TruncatedSVDApproximation" in source
    assert "from manim" not in source
    assert "import manim" not in source
