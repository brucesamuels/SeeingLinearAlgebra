# CP91 — Revised Chapter 1 Assembly

## Goal

Build the complete current Chapter 1 from the approved standalone lesson scenes.
The assembly now includes the dot-product and cross-product lessons developed in
CP88–CP90.

## Chapter sequence

1. Chapter title card
2. Why Vectors?
3. What Is a Vector?
4. Free Vectors and Equality
5. Placing a Vector at the Origin
6. Special Vectors
7. Scalar Multiplication
8. Unit Vectors
9. Vector Addition
10. Commutativity of Vector Addition
11. Vector Subtraction
12. Three-Vector Addition in 3D
13. Infinite Possibilities
14. Inner Products and the Dot Product
15. The Cross Product
16. Computing the Cross Product

## Implementation

- `engine/chapter_one_lesson_manifest.py` defines the complete approved order.
- `scripts/build_cp91_chapter_one.py` locates and renders every standalone lesson
  scene, then concatenates the MP4 files with `ffmpeg`.
- The legacy combined `ChapterOneOpeningPresentation` is not used.
- The completed video is written to:

  `media/videos/chapter_one_assembly/480p15/ChapterOneAssembly.mp4`

## Validation

The installer runs the focused CP91 assembly test file. The tests verify:

- the complete 15-lesson manifest,
- placement of the dot-product and cross-product lessons at the chapter end,
- exact CP88–CP90 scene filenames,
- scene discovery,
- the title card,
- the standalone-scene render strategy,
- and the final output path.

Do not commit until the complete chapter render is visually approved.

## v6 packaging correction

- Corrects the multiline scene fixture in the CP91 test module.
- Adds Python syntax compilation before focused tests run.


## v7 scene-discovery correction

- Expands scene discovery from only `*_presentation.py` files to all Python
  files in the `scenes` directory.
- Adds explicit aliases for the approved Unit Vector lesson filename variants.
- Adds regression tests for `unit_vector_lesson.py` and the broader fallback.

## v8 scene discovery fix

- Replaces filename guessing with semantic discovery using class names, `TITLE` text, filenames, and scene source.
- Adds regression coverage for an unexpectedly named Unit Vectors scene.
- Improves failure diagnostics by listing all available scene files.


## v9 locator correction

- Normalizes simple trailing-s plurals during semantic scene discovery.
- Allows a scene titled `Unit Vectors` to satisfy the manifest token `unit vector`.
- Adds a regression test for singular/plural title matching.
