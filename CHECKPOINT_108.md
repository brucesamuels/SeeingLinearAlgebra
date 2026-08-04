# Checkpoint 108 — Why Row Replacement Preserves Solutions

## Purpose

Checkpoint 108 explains why the elementary operation

\[
R_i\leftarrow R_i+cR_j
\]

preserves the solution set of a linear system.

The lesson uses

\[
x+y=2,
\qquad
2x-y=1,
\]

and the replacement

\[
R_2\leftarrow R_2-2R_1.
\]

The transformed second equation is

\[
-3y=-3.
\]

## Mathematical idea

The proof has two directions.

1. Any solution of the original equations also satisfies the replacement equation, because a linear combination of true equations is true.
2. The original row can be recovered by the inverse operation

   \[
   R_2\leftarrow R_2+2R_1.
   \]

Therefore no information is lost and both systems have exactly the same solution set.

## Files

- `engine/row_replacement_preserves_solutions.py`
- `scenes/row_replacement_preserves_solutions_presentation.py`
- `tests/test_row_replacement_preserves_solutions.py`
- `tests/test_row_replacement_preserves_solutions_presentation.py`
- `scripts/check_cp108_row_replacement_preserves_solutions.zsh`
- `scripts/render_cp108_row_replacement_preserves_solutions.zsh`

## Check

```zsh
./scripts/check_cp108_row_replacement_preserves_solutions.zsh
```

## Render

```zsh
./scripts/render_cp108_row_replacement_preserves_solutions.zsh
```
