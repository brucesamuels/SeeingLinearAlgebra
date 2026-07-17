# Engine v0.3 - Checkpoint 34

## Goal

Integrate the renderer-independent `LessonSequence` metadata from Checkpoint 33
into exactly one existing full-rank 3D presentation scene without changing
rendered behavior.

## Change

Checkpoint 34 adds one reusable lesson declaration:

```python
FULL_RANK_3D_LESSON_SEQUENCE = LessonSequence(
    (
        LessonBeat("establish_3d_frame", LessonBeatRole.ORIENT),
        LessonBeat("predict_combination_motion", LessonBeatRole.PREDICT),
        LessonBeat(
            "animate_independent_coefficients",
            LessonBeatRole.OBSERVE,
        ),
        LessonBeat("pin_exact_final_state", LessonBeatRole.STABILIZE),
        LessonBeat("reflect_on_full_rank_span", LessonBeatRole.REFLECT),
    )
)
```

The existing scene receives only:

```python
from engine.full_rank_3d_lesson_sequence import (
    FULL_RANK_3D_LESSON_SEQUENCE,
)
```

and one class-level declaration:

```python
LESSON_SEQUENCE = FULL_RANK_3D_LESSON_SEQUENCE
```

Its explicit `construct()` method remains unchanged.

## Repository-aware installation

The exact Checkpoint 32 scene filename was not available to the packaging
environment. The installer therefore searches the local repository for the
single high-confidence `ThreeDScene` matching the full-rank 3D presentation.

It validates the Python AST before and after modification and refuses to act
when:

- Checkpoint 33 is missing;
- no credible scene is found;
- more than one scene has the same best score;
- the selected scene already declares `LESSON_SEQUENCE`;
- any additive destination already exists.

The installer creates a temporary backup of the selected scene and restores it
if any later installation step fails.

## Responsibility boundary

The metadata describes:

- orientation;
- prediction;
- observation;
- exact-state stabilization;
- conceptual reflection.

It does not:

- call scene methods;
- register callbacks;
- contain animations or durations;
- modify coefficient paths;
- modify matrices or geometry;
- control camera motion;
- inspect `construct()` execution order;
- create a timeline or chapter framework.

## Files

Additive:

```text
CHECKPOINT_34.md
engine/full_rank_3d_lesson_sequence.py
tests/test_full_rank_3d_lesson_sequence.py
scripts/check_full_rank_3d_lesson_sequence.zsh
```

Narrow modification:

```text
one existing full-rank 3D presentation scene
```

The installer adds only one import and one class attribute to that scene.

## Tests

The focused tests verify:

- the declared beat names;
- the ordered pedagogical roles;
- the scene exposes a real `LessonSequence`;
- the scene references the canonical sequence object;
- the scene still owns an explicit `construct()` implementation.

The tests deliberately do not introspect animation order or execute the
sequence.

## Render decision

No render is required because no statement inside `construct()` changes and no
renderer object is added.

## Next checkpoint

Checkpoint 35 should apply lesson-sequence metadata to a second, meaningfully
different lesson scene. The second adoption should test whether the five-role
vocabulary generalizes without extending or weakening it prematurely.
