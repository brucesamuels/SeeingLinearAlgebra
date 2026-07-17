# Engine v0.3 - Checkpoint 33

## Goal

Introduce the smallest renderer-independent abstraction justified by the
pedagogical sequencing now repeated across the presentation scenes:

```text
LessonBeat
LessonBeatRole
LessonSequence
```

Checkpoint 33 records instructional structure without executing it.

## Architectural finding

The completed presentation work now demonstrates a recurring progression:

```text
orient -> predict -> observe -> stabilize -> reflect
```

The repetition is pedagogical rather than mathematical or renderer-specific.

The correct first extraction is therefore immutable lesson metadata, not:

- an animation timeline;
- a callback runner;
- a scene dispatcher;
- a scripting language;
- a lesson superclass;
- a chapter framework.

## Public interface

```python
from engine.lesson_sequence import (
    LessonBeat,
    LessonBeatRole,
    LessonSequence,
)

LINEAR_COMBINATION_LESSON = LessonSequence(
    (
        LessonBeat("establish_frame", LessonBeatRole.ORIENT),
        LessonBeat("pause_and_predict", LessonBeatRole.PREDICT),
        LessonBeat("coefficient_sweep", LessonBeatRole.OBSERVE),
        LessonBeat("pin_exact_endpoint", LessonBeatRole.STABILIZE),
        LessonBeat("span_reflection", LessonBeatRole.REFLECT),
    )
)
```

A renderer-specific scene may expose this sequence as class-level metadata while
keeping its `construct()` implementation explicit:

```python
class LinearCombinationPresentation(Scene):
    LESSON_SEQUENCE = LINEAR_COMBINATION_LESSON

    def construct(self):
        self.establish_frame()
        self.show_prediction()
        self.run_coefficient_sweep()
        self.pin_exact_endpoint()
        self.show_reflection()
```

Checkpoint 33 does not require existing scenes to adopt the metadata. The
abstraction is proved independently first.

## Roles

The initial vocabulary is deliberately narrow:

```text
ORIENT
PREDICT
OBSERVE
STABILIZE
REFLECT
```

These roles describe instructional intent, not animation type.

A lesson may contain more than one beat with the same role. The abstraction
does not impose a mandatory canonical order because future lessons may revisit,
branch conceptually, or omit a role.

## Responsibility boundary

`LessonBeat` owns:

- one normalized nonempty name;
- one valid pedagogical role.

`LessonSequence` owns:

- immutable declared beat order;
- unique beat names;
- lookup by name;
- role-based inspection;
- basic collection behavior.

The module does not own:

- mathematical snapshots;
- coefficients or vector arithmetic;
- geometry;
- projection;
- Manim mobjects;
- animations;
- callbacks;
- durations;
- narration;
- camera movement;
- layout;
- scene execution;
- chapter composition.

## Why no automatic runner

An API such as:

```python
LessonSequence.run(scene)
```

would require callbacks or method-name dispatch and would begin to hide
`scene.play(...)`, updater ownership, endpoint pinning, camera behavior, and
renderer lifecycle decisions.

Those concerns remain explicit in each thin final scene adapter.

## Compatibility

All files are additive:

```text
CHECKPOINT_33.md
engine/lesson_sequence.py
tests/test_lesson_sequence.py
scripts/check_lesson_sequence.zsh
```

Checkpoint 33 intentionally does not modify:

```text
engine/__init__.py
existing mathematics modules
existing geometry modules
existing projection modules
existing Manim adapters
existing scenes
existing render scripts
```

No render script is added because this checkpoint changes no rendered behavior.

## Focused verification

The tests verify:

- stable pedagogical role values;
- frozen lesson beats;
- normalized nonempty names;
- valid role enforcement;
- nonempty lesson sequences;
- unique beat names;
- exact order preservation;
- immutable tuple exposure;
- lookup and membership behavior;
- ordered role filtering;
- independence of distinct sequences;
- import without Manim;
- import without NumPy.

The checkpoint script runs the focused tests first and then the complete
repository suite.

## Installation

From the repository root, copy the checkpoint files into place, make the script
executable, and run:

```zsh
chmod +x scripts/check_lesson_sequence.zsh
./scripts/check_lesson_sequence.zsh
```

## Expected test count

The repository had 425 passing tests after Checkpoint 32.

This checkpoint adds 21 focused tests, so the expected total is approximately:

```text
446 passed
```

The exact count may differ if the local Checkpoint 32 repository already
contains additional parametrized cases.

## Architectural result

After Checkpoint 33 the separation remains:

```text
mathematics
    ↓
geometry
    ↓
projection
    ↓
presentation adapters
    ↓
scene-owned execution

lesson-sequence metadata describes the pedagogical intent alongside this
pipeline without controlling any layer.
```

## Next checkpoint

Checkpoint 34 should integrate lesson-sequence metadata into one existing
presentation scene only if the Checkpoint 33 abstraction passes cleanly.

That integration should:

- add one class-level sequence declaration;
- preserve the scene's explicit `construct()` flow;
- add no execution engine;
- change no rendered behavior;
- verify that the declared beat names correspond to meaningful scene-level
  operations.

A second scene should adopt the same abstraction only after the first
integration is proven. A chapter framework remains premature.
