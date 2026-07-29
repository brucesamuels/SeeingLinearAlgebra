# Checkpoint 81.3 — Opening Wrap, Chapter-Level Slowdown, and Narration Script

## Goals
- Keep the chapter-opening question on screen.
- Slow the complete chapter without regenerating every Manim scene.
- Provide a proposed narration script for the assembled animation.

## Opening card
The chapter question is explicitly wrapped into two lines and reduced slightly in size.

## Chapter-level pacing
The PyAV assembler now accepts a duration multiplier. A multiplier of `1.25` makes the chapter 25 percent longer by duplicating frames during assembly. The individual Manim scenes are not regenerated.

The normal render script now defaults to a duration factor of `1.25`.

A separate script reassembles already-rendered chapter segments:

```zsh
./scripts/reassemble_vector_spaces_chapter.zsh
```

An alternative duration can be supplied:

```zsh
./scripts/reassemble_vector_spaces_chapter.zsh 1.4
```

## Narration
`CHAPTER_2_NARRATION_SCRIPT.md` proposes narration for:
- the opening,
- dependence and subspaces,
- basis and dimension,
- the matrix subspaces,
- rank-nullity,
- the four fundamental subspaces,
- the closing transition to linear transformations.

## Files updated or added
- `scenes/vector_spaces_chapter_cards.py`
- `scripts/assemble_vector_spaces_chapter.py`
- `scripts/render_vector_spaces_chapter.zsh`
- `scripts/reassemble_vector_spaces_chapter.zsh`
- `tests/test_vector_spaces_chapter_pacing.py`
- `CHAPTER_2_NARRATION_SCRIPT.md`
- `CHECKPOINT_81_3.md`
