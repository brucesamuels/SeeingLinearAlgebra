from __future__ import annotations

import dataclasses
import importlib
import sys

import pytest

from engine.lesson_sequence import LessonBeat, LessonBeatRole, LessonSequence


def sample_sequence() -> LessonSequence:
    return LessonSequence(
        (
            LessonBeat("establish_frame", LessonBeatRole.ORIENT),
            LessonBeat("pause_and_predict", LessonBeatRole.PREDICT),
            LessonBeat("coefficient_sweep", LessonBeatRole.OBSERVE),
            LessonBeat("pin_exact_endpoint", LessonBeatRole.STABILIZE),
            LessonBeat("span_reflection", LessonBeatRole.REFLECT),
        )
    )


def test_roles_are_stable_string_enum_values() -> None:
    assert tuple(role.value for role in LessonBeatRole) == (
        "orient",
        "predict",
        "observe",
        "stabilize",
        "reflect",
    )


def test_lesson_beat_is_frozen_and_normalizes_name() -> None:
    beat = LessonBeat("  establish_frame  ", LessonBeatRole.ORIENT)

    assert beat.name == "establish_frame"
    assert beat.role is LessonBeatRole.ORIENT

    with pytest.raises(dataclasses.FrozenInstanceError):
        beat.name = "changed"  # type: ignore[misc]


@pytest.mark.parametrize("name", ["", " ", "\n\t"])
def test_lesson_beat_rejects_empty_name(name: str) -> None:
    with pytest.raises(ValueError, match="nonempty"):
        LessonBeat(name, LessonBeatRole.ORIENT)


def test_lesson_beat_rejects_nonstring_name() -> None:
    with pytest.raises(TypeError, match="string"):
        LessonBeat(3, LessonBeatRole.ORIENT)  # type: ignore[arg-type]


def test_lesson_beat_rejects_invalid_role() -> None:
    with pytest.raises(TypeError, match="LessonBeatRole"):
        LessonBeat("frame", "orient")  # type: ignore[arg-type]


def test_sequence_preserves_exact_order_and_identity() -> None:
    beats = (
        LessonBeat("frame", LessonBeatRole.ORIENT),
        LessonBeat("question", LessonBeatRole.PREDICT),
        LessonBeat("motion", LessonBeatRole.OBSERVE),
    )
    sequence = LessonSequence(beats)

    assert sequence.beats == beats
    assert sequence[0] is beats[0]
    assert tuple(sequence) == beats
    assert len(sequence) == 3


def test_sequence_exposes_ordered_names_and_roles() -> None:
    sequence = sample_sequence()

    assert sequence.names == (
        "establish_frame",
        "pause_and_predict",
        "coefficient_sweep",
        "pin_exact_endpoint",
        "span_reflection",
    )
    assert sequence.roles == (
        LessonBeatRole.ORIENT,
        LessonBeatRole.PREDICT,
        LessonBeatRole.OBSERVE,
        LessonBeatRole.STABILIZE,
        LessonBeatRole.REFLECT,
    )


def test_sequence_lookup_returns_original_beat() -> None:
    sequence = sample_sequence()

    assert sequence.beat(" coefficient_sweep ") is sequence[2]
    assert sequence.has_beat("coefficient_sweep")
    assert "coefficient_sweep" in sequence
    assert "missing" not in sequence


def test_unknown_lookup_raises_clear_key_error() -> None:
    sequence = sample_sequence()

    with pytest.raises(KeyError, match="unknown lesson beat"):
        sequence.beat("missing")


@pytest.mark.parametrize("name", ["", " ", "\n"])
def test_empty_lookup_name_is_rejected(name: str) -> None:
    sequence = sample_sequence()

    with pytest.raises(ValueError, match="nonempty"):
        sequence.beat(name)


def test_role_filter_preserves_declared_order() -> None:
    first = LessonBeat("first_observation", LessonBeatRole.OBSERVE)
    second = LessonBeat("second_observation", LessonBeatRole.OBSERVE)
    sequence = LessonSequence(
        (
            LessonBeat("frame", LessonBeatRole.ORIENT),
            first,
            LessonBeat("question", LessonBeatRole.PREDICT),
            second,
        )
    )

    assert sequence.beats_with_role(LessonBeatRole.OBSERVE) == (first, second)


def test_sequence_requires_at_least_one_beat() -> None:
    with pytest.raises(ValueError, match="at least one"):
        LessonSequence(())


def test_sequence_rejects_nonbeat_entries() -> None:
    with pytest.raises(TypeError, match="LessonBeat"):
        LessonSequence((LessonBeat("frame", LessonBeatRole.ORIENT), "bad"))


def test_sequence_rejects_duplicate_normalized_names() -> None:
    with pytest.raises(ValueError, match="unique"):
        LessonSequence(
            (
                LessonBeat("frame", LessonBeatRole.ORIENT),
                LessonBeat(" frame ", LessonBeatRole.REFLECT),
            )
        )


def test_sequence_state_is_immutable_from_public_surface() -> None:
    sequence = sample_sequence()

    assert isinstance(sequence.beats, tuple)

    with pytest.raises(AttributeError):
        sequence.beats = ()  # type: ignore[misc]

    with pytest.raises(TypeError):
        sequence.beats[0] = LessonBeat(  # type: ignore[index]
            "replacement", LessonBeatRole.ORIENT
        )


def test_distinct_sequences_share_no_mutable_state() -> None:
    first = sample_sequence()
    second = sample_sequence()

    assert first is not second
    assert first.beats == second.beats
    assert first._beats_by_name is not second._beats_by_name


def test_module_imports_without_manim_or_numpy() -> None:
    sys.modules.pop("engine.lesson_sequence", None)
    before = set(sys.modules)

    module = importlib.import_module("engine.lesson_sequence")
    imported = set(sys.modules) - before

    assert module.LessonSequence is not None
    assert not any(name == "manim" or name.startswith("manim.") for name in imported)
    assert not any(name == "numpy" or name.startswith("numpy.") for name in imported)
