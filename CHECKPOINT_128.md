# Checkpoint 128 - Why Do We Need Determinants?

## Purpose

Open Chapter 5 with the geometric problem that determinants answer:

> How does a linear transformation change area or volume?

This lesson introduces the determinant as one signed scale factor that records three kinds of behavior:

1. expansion or contraction;
2. preservation or reversal of orientation;
3. collapse into a lower-dimensional set.

The coordinate formula for a 2 x 2 determinant is intentionally absent. CP129 will focus on area scale, CP130 on sign and orientation, and CP131 will derive the formula from geometry.

## Mathematical narrative

A single reference square remains in one stable coordinate system. Four maps are applied in sequence:

| Purpose | Matrix | Signed scale | Visual effect |
|---|---:|---:|---|
| Expand | `[[2, 1], [0, 1]]` | `+2` | square becomes an area-2 parallelogram |
| Contract | `[[1, 0], [0, 1/2]]` | `+1/2` | height and area are halved |
| Reverse | `[[-1, 0], [0, 1]]` | `-1` | area magnitude is preserved while orientation reverses |
| Collapse | `[[1, 2], [0, 0]]` | `0` | the region collapses onto a line |

The lesson closes by naming the determinant, not by computing it from entries.

## Architecture decisions

- `engine/determinant_need.py` is renderer-independent and computes transformed polygons and signed polygon areas.
- The engine uses signed shoelace area to support the visual narrative without preempting the later derivation of `ad - bc`.
- `scenes/why_determinants_presentation.py` uses one coordinate system for visual stability.
- The lesson is 2D. A 3D camera is deferred until CP135, where volume genuinely requires it.
- The four-example sequence becomes a chapter-wide vocabulary: magnitude, sign, and zero.

## Files

- `engine/determinant_need.py`
- `scenes/why_determinants_presentation.py`
- `tests/test_determinant_need.py`
- `tests/test_why_determinants_presentation.py`
- `scripts/check_cp128_why_determinants.zsh`
- `scripts/render_cp128_why_determinants.zsh`
- `CHECKPOINT_128.md`

## Install

From the repository root:

```zsh
unzip -q ~/Downloads/seeing_linear_algebra_cp128.zip -d /tmp/seeing_linear_algebra_cp128
zsh /tmp/seeing_linear_algebra_cp128/apply_checkpoint_128.zsh
```

The installer rejects unrelated tracked or untracked repository changes. It permits replacement of files belonging to CP128, so a revised CP128 package can be applied safely before commit.

## Check

```zsh
zsh scripts/check_cp128_why_determinants.zsh
```

## Render

Preview:

```zsh
zsh scripts/render_cp128_why_determinants.zsh -pql
```

High quality after preview approval:

```zsh
zsh scripts/render_cp128_why_determinants.zsh -pqh
```

## Visual review checklist

- The title and subtitle remain inside the frame.
- The coordinate axes do not move between examples.
- The transformed region is visibly distinct in all four examples.
- The collapse example reads as a line rather than a malformed filled polygon.
- Matrix, caption, and signed-scale label do not collide.
- The final central question has comfortable margins and sufficient reading time.
- No `ad - bc` formula appears.

Do not commit until the preview has been visually approved.
