# Engine Architecture

```text
SeeingMathematics/
├── assets/
├── docs/
├── engine/
├── episodes/
├── scripts/
├── tests/
└── media_exports/
```

## Engine v0.1

- `theme.py`: colors, font sizes, spacing, and timing.
- `branding.py`: Brooklyn Tech intro and closing cards.
- `scene_tools.py`: mixed-object cleanup, title bands, and pause cards.

## Planned next modules

- `vectors.py`: 2D/3D vectors, translated copies, scalar multiples, addition.
- `spans.py`: span line, plane, volume, coefficient sweeps, rank collapse.
- `matrices.py`: column matrices, coefficient vectors, column-space reveal.

## Import rule

Render from the repository root:

```zsh
python3 -m manim -pql episodes/02_span_rank_dimension/episode.py Episode02
```

Episodes import reusable components only from `engine`.

## Stability rule

Never replace the permanent repository folder. Update individual files inside it.
