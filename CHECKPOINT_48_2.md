# Checkpoint 48.2 - Lesson Layout Manager

## Goal

Introduce a reusable renderer-side lesson layout with stable screen regions:

```text
TITLE
QUESTION
CONTENT
FOOTER
```

The layout keeps the main instructional block in an upper-left safe area and
reserves the lower screen for synthesis, reflection, narration, or transitions.

## New abstraction

```text
LessonLayout
```

It provides:

- title anchor;
- guiding-question anchor;
- content anchor;
- footer anchor;
- standard text scales;
- automatic height fitting for content blocks.

## Why this is renderer-side

The layout controls screen composition only. It contains no:

- mathematics;
- lesson content;
- animation timing;
- chapter sequencing;
- pedagogical semantics.

## CP48 integration

The `WhyVectorsPresentation` now uses the shared layout for:

- the fixed title;
- the fixed guiding question;
- each perspective content block;
- the final bridge statement;
- the synthesis footer.

Application rows are left aligned and scaled to remain inside the safe content
region.

## Verification

```zsh
./scripts/check_why_vectors.zsh
python -m pytest -q \
  tests/test_manim_lesson_layout.py \
  tests/test_why_vectors_layout_refinement.py
./scripts/render_why_vectors.zsh
```
