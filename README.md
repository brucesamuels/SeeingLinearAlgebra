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

## Production environment

- macOS
- zsh
- Python 3.12
- Manim Community 0.21.0

### Manim 0.21.0 compatibility audit

The project was migrated from Manim Community 0.20.1 to 0.21.0 after a compatibility audit.

Validation results:

- 2753 tests passed under Manim 0.21.0
- No project or Manim deprecation warnings were found
- The remaining warning comes from `pydub` importing Python's deprecated `audioop` module
- Representative matrix, vector, 3D, eigenvalue, and Change of Basis scenes rendered successfully
- Manim 0.20.1 remains the previously validated production baseline for earlier checkpoints

All Manim commands should be run from the repository root.

For the current Conda environment:

    conda activate seeingla-manim021
    export PYTHONPATH="$PWD"

