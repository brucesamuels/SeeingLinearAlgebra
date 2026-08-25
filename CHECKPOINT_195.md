# Checkpoint 195 — Coordinates as Linear-Combination Recipes

This lesson is the conceptual bridge between coordinates relative to a basis and basis matrices.

## Learning objective

Students see that changing coordinates means rewriting the same geometric vector as a linear combination of different basis vectors. The coefficients of those linear combinations become coordinate columns, and the coordinate recipes for the basis vectors become the columns of a basis or transition matrix.

## Numerical story

- Standard basis: `E = (e1,e2)`
- New basis: `B = (b1,b2)` with `b1=(1,0)` and `b2=(1,1)`
- Fixed vector: `v=(3,2)`
- Standard recipe: `v=3e1+2e2`, so `[v]_E=(3,2)`
- B-recipe: `v=b1+2b2`, so `[v]_B=(1,2)`
- Basis-vector recipes: `[b1]_E=(1,0)` and `[b2]_E=(1,1)`
- Basis matrix: `P_B=[[1,1],[0,1]]`
- Conversion: `[v]_E=P_B[v]_B`

The final card previews the general transition matrix by placing `[b1]_C` and `[b2]_C` in its columns.

## Placement

Place this lesson after **Coordinates Relative to a Basis** and before **The Basis Matrix**.

## Commands

```zsh
zsh scripts/check_cp195_coordinate_linear_combinations.zsh
zsh scripts/render_cp195_coordinate_linear_combinations.zsh
```

