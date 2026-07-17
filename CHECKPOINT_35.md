# Engine v0.3 - Checkpoint 35

## Goal

Adopt the renderer-independent lesson-sequence abstraction in a second,
meaningfully different presentation scene.

Checkpoint 34 demonstrated that metadata could be attached to the full-rank 3D
linear-combination lesson without changing rendering. Checkpoint 35 tests
whether the same pedagogical vocabulary generalizes to rank collapse.

## Rank-collapse declaration

```python
RANK_COLLAPSE_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat(
            "establish_initial_geometry",
            LessonBeatRole.ORIENT,
        ),
        LessonBeat(
            "predict_rank_loss",
            LessonBeatRole.PREDICT,
        ),
        LessonBeat(
            "animate_rank_collapse",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat(
            "stabilize_degenerate_state",
            LessonBeatRole.STABILIZE,
        ),
        LessonBeat(
            "reflect_on_dimension_loss",
            LessonBeatRole.REFLECT,
        ),
    )
)
```

The semantic roles remain unchanged:

```text
ORIENT -> PREDICT -> OBSERVE -> STABILIZE -> REFLECT
```

The beat names remain lesson-specific.

## Architectural evidence

The two lessons now describe different mathematical narratives:

```text
Full-rank 3D:
independent coefficient motion and construction of a vector in a full span

Rank collapse:
loss of dimensional freedom and stabilization at a degenerate image
```

They use the same pedagogical roles without sharing lesson-specific beat names.

That is evidence that `LessonBeatRole` describes reusable educational intent
rather than one animation or one mathematical pipeline.

## Scene modification

The selected rank-collapse presentation scene receives only:

```python
from engine.rank_collapse_lesson_sequence import (
    RANK_COLLAPSE_LESSON_SEQUENCE,
)
```

and:

```python
LESSON_SEQUENCE = RANK_COLLAPSE_LESSON_SEQUENCE
```

Its explicit `construct()` method remains unchanged.

## Repository-aware installer

The packaging environment did not contain the current local repository. The
installer therefore locates the single high-confidence rank-collapse
presentation scene using:

- filename evidence;
- class-name evidence;
- `Scene` or `ThreeDScene` inheritance;
- rank-collapse terminology;
- presentation markers;
- penalties for smoke and geometry-only classes.

It refuses to modify anything if the best match is absent, ambiguous, or below
the confidence threshold.

A temporary backup is restored automatically if a later installation step
fails.

## Files

Additive:

```text
CHECKPOINT_35.md
engine/rank_collapse_lesson_sequence.py
tests/test_rank_collapse_lesson_sequence.py
scripts/check_rank_collapse_lesson_sequence.zsh
```

Narrow modification:

```text
one existing rank-collapse presentation scene
```

## Focused tests

The four focused tests verify:

- exact rank-collapse beat names and roles;
- attachment of the canonical sequence to the scene;
- continued ownership of an explicit `construct()` method;
- reuse of the same role vocabulary as the full-rank 3D lesson;
- separation of lesson-specific beat names.

## Deliberate omissions

Checkpoint 35 does not add:

- roles;
- callbacks;
- timing metadata;
- automatic dispatch;
- render-order introspection;
- scene inheritance;
- timeline execution;
- lesson or chapter frameworks.

## Render decision

No render is required because the selected scene receives only metadata. The
body of `construct()` is unchanged.

## Expected test count

Checkpoint 34 was expected to leave approximately 449 passing tests.
Checkpoint 35 adds four focused tests, for an expected total near:

```text
453 passed
```

The exact count depends on the local repository.

## Architectural result

With two substantially different lessons using the same role vocabulary, the
initial `LessonSequence` API has earned a stability period.

The next checkpoint should not extend it. A useful next step is lightweight
inspection or documentation tooling that reads existing lesson metadata without
influencing scene execution.
