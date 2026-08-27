# Checkpoint 198 — Change of Basis High-Definition Master

This checkpoint renders the complete Change of Basis chapter at 1080p60, assembles a normal-speed master, and creates a slowed classroom master.

## Production settings

- Manim quality: `-qh` (`1080p60`)
- Cache: disabled so every lesson is freshly rendered
- Playback speed: `0.85`
- Slowdown method: applied after chapter assembly
- Video encoding: H.264, CRF 18, 60 fps
- Audio, if later present: slowed with `atempo=0.85`

## Verified lesson order

1. Chapter title
2. Why Change Basis
3. Coordinates Relative to a Basis
4. Coordinates as Linear-Combination Recipes
5. The Basis Matrix
6. Standard to Basis Coordinates
7. Changing Between Two Nonstandard Bases
8. Matrix of a Transformation in Another Basis
9. Changing a Transformation Between Two Bases
10. Why a Good Basis Matters
11. One Object, Many Descriptions

## Commands

```zsh
zsh scripts/check_cp198_change_of_basis_master.zsh
zsh scripts/render_cp198_change_of_basis_master.zsh
```

## Outputs

```text
media/change_of_basis_master.mp4
media/change_of_basis_master_85pct.mp4
```

The second file is the recommended classroom master.

