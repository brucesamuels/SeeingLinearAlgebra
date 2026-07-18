# Engine v0.3 — Checkpoint 53

## Chapter 1 opening Manim orchestration

Checkpoint 53 adds the first combined renderer-side presentation for Chapter 1.
It consumes the renderer-independent lesson order introduced in Checkpoint 52
and delegates each lesson to its already approved standalone Manim scene.

## Added files

- `scenes/chapter_one_opening_presentation.py`
- `tests/test_chapter_one_opening_presentation.py`
- `scripts/check_chapter_one_opening_presentation.zsh`
- `scripts/render_chapter_one_opening_presentation.zsh`

## Presentation order

The combined scene renders:

1. `WhyVectorsPresentation`
2. `VectorRepresentationPresentation`
3. `FreeVectorEqualityPresentation`

The order is not duplicated as an independent tuple. The scene iterates over
`CHAPTER_ONE_OPENING_SEQUENCE` and resolves each lesson key through a read-only
renderer-side presentation registry.

## Architectural boundary

This checkpoint intentionally introduces no general-purpose chapter renderer.
It first proves that completed lesson scenes can share one Manim lifecycle and
one canvas without changing their approved standalone implementations.

`ChapterOneOpeningPresentation` is therefore a small adapter that:

- inherits the renderer helpers already used by `WhyVectorsPresentation`;
- delegates to each existing lesson's `construct` method;
- creates a named Manim section for each renderer-independent lesson key;
- fades and clears the canvas only between lessons;
- preserves each standalone presentation as an independent render target.

No lesson mathematics, geometry, pedagogy, timing, or visual-identity code is
copied into the combined scene.

## Verification

Run:

```zsh
./scripts/check_chapter_one_opening_presentation.zsh
```

Then render the combined opening:

```zsh
./scripts/render_chapter_one_opening_presentation.zsh
```

The render is the architectural experiment for this checkpoint. Review the
lesson boundaries, residual mobjects, title continuity, pacing, and whether the
three standalone scenes feel coherent when viewed as one chapter opening.

## Next architectural decision

After the combined render succeeds, use the visual evidence to decide whether
Checkpoint 54 should:

- refine the chapter boundary transitions first; or
- add the next proven lesson, Vector Addition, before extracting a reusable
  chapter-presentation abstraction.
