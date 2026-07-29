# Checkpoint 81 — Assemble the Vector Spaces and Subspaces Chapter

## Goal
Create a conservative first assembly of the completed vector-spaces/subspaces lessons before beginning linear transformations.

This checkpoint does not rewrite the individual lessons. It establishes a provisional order, adds chapter and section cards, renders each existing lesson, and concatenates the results into one low-quality review video.

## Chapter title
**Vector Spaces: Structure, Dimension, and the Spaces Inside a Matrix**

## Opening question
> What makes a collection of vectors into a space, and how can a matrix reveal its hidden structure?

## Provisional chapter order

### Opening
1. Chapter opening

### Part I — From Dependence to Subspaces
2. When Space Collapses
3. The Subspace Test

### Part II — Basis and Dimension
4. Basis and Dimension

### Part III — The Spaces Inside a Matrix
5. Column Space
6. Null Space
7. Row Space
8. Pivot Columns

### Part IV — How the Dimensions Fit Together
9. Rank and Nullity
10. The Four Fundamental Subspaces

### Closing
11. Chapter reflection

## Closing reflection
> A matrix organizes directions into what survives, what disappears, what can be produced, and what remains unreachable.

## Render strategy
- Render the chapter cards and existing lesson scenes at low quality.
- Keep each lesson as its own scene and media segment.
- Concatenate the MP4 segments with `ffmpeg`.
- Review the combined chapter for pacing, repetition, terminology, transitions, and missing conceptual bridges.

## Output
`media/videos/vector_spaces_chapter/480p15/VectorSpacesAndSubspacesChapter.mp4`

## Files added
- `engine/vector_spaces_chapter.py`
- `scenes/vector_spaces_chapter_cards.py`
- `tests/test_vector_spaces_chapter.py`
- `tests/test_vector_spaces_chapter_cards.py`
- `tests/test_vector_spaces_chapter_render_script.py`
- `scripts/check_vector_spaces_chapter.zsh`
- `scripts/render_vector_spaces_chapter.zsh`
- `CHECKPOINT_81.md`
