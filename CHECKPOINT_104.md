# Checkpoint 104 — Matrix Operations Chapter Assembly

## Chapter order

1. Opening card
2. Matrix Addition and Subtraction
3. Scalar Multiplication of Matrices
4. Matrix–Vector Multiplication as a Column Combination
5. The Row–Column Rule
6. Matrix–Matrix Multiplication
7. Matrix Multiplication as Composition
8. The Trace of a Matrix
9. Matrix Transposition
10. Order, Identity, and Undoing
11. Closing reflection

## New material

- `MatrixOperationsChapterTitleCard`
- `MatrixOperationsChapterReflectionCard`
- a robust assembly script that discovers the historical CP94 column-combination
  scene by content;
- complete chapter rendering and ffmpeg concatenation;
- an optional mode that reuses existing lesson renders.

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp104/apply_checkpoint_104.zsh
~/Downloads/seeing_linear_algebra_cp104/apply_checkpoint_104.zsh
```

## Check

Run the package test and the complete repository suite:

```zsh
./scripts/check_cp104_matrix_operations_chapter.zsh
```

## Render the complete chapter

For a clean render of every scene:

```zsh
./scripts/render_cp104_matrix_operations_chapter.zsh
```

To reuse existing lesson renders and render only missing scenes:

```zsh
./scripts/render_cp104_matrix_operations_chapter_reuse.zsh
```

## Output

The assembled chapter is written to:

```text
media/videos/matrix_operations_chapter/MatrixOperationsChapter.mp4
```

Review the complete chapter before committing.
