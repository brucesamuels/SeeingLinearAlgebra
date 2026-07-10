# Seeing Linear Algebra

A visual linear algebra series produced for Brooklyn Technical High School.

## Current episodes

- Episode 1: Vectors, Magnitude, Unit Vectors, Coordinates, and Span
- Episode 2: Span and Vector Subspaces

## Project root

All Manim commands should be run from the project root so imports from `common` work correctly.

```zsh
cd ~/Documents/School/'Linear Algebra'/SeeingLinearAlgebra
```

## Render Episode 1 preview

```zsh
python3 -m manim -pql episode01_vectors/episode01.py Episode01Vectors
```

## Render Episode 2 preview

```zsh
python3 -m manim -pql episode02_subspaces/episode02.py Episode02Subspaces
```

## HD renders

```zsh
python3 -m manim -pqh episode01_vectors/episode01.py Episode01Vectors
python3 -m manim -pqh episode02_subspaces/episode02.py Episode02Subspaces
```

See `GIT_WORKFLOW.md` for the version-control procedure.
