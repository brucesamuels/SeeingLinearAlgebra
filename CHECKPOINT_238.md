# Checkpoint 238 — Directed Graphs and PageRank

This checkpoint changes the recurring graph's edges into directed links and
uses a random walk to build a ranking. It introduces source, destination,
out-degree, dangling vertices, link matrices, dangling-column repair,
teleportation, the Google matrix, and PageRank from first principles.

## Directed graph and convention

The four vertices retain the recurring graph's underlying skeleton, but the
edges now have directions:

```text
1 -> 2,  2 -> 3,  3 -> 1,  3 -> 4.
```

Thus the triangle is a directed cycle, vertex 3 has two outgoing links, and
vertex 4 has none. As in CP236, distributions are columns and matrix column `j`
describes movement away from source vertex `j`.

The raw link matrix is

```text
    [0 0 1/2 0]
H = [1 0  0  0]
    [0 1  0  0]
    [0 0 1/2 0].
```

Its fourth column sums to zero, so an unmodified walk would lose probability at
vertex 4. Replace that column by `(1/4,1/4,1/4,1/4)^T` to form the repaired link
matrix `S`.

## Teleportation and exact PageRank spine

For introductory arithmetic, choose the link-following probability
`alpha=1/2`. With the remaining probability, jump uniformly to any vertex:

```text
G = (1/2) S + (1/2) U,       U = (1/4) 1 1^T.
```

Therefore

```text
    [1/8 1/8 3/8 1/4]
G = [5/8 1/8 1/8 1/4]
    [1/8 5/8 1/8 1/4]
    [1/8 1/8 3/8 1/4].
```

Starting uniformly gives

```text
p0 = (1/4,1/4,1/4,1/4)^T
p1 = (7/32,9/32,9/32,7/32)^T
p2 = (57/256,67/256,75/256,57/256)^T.
```

The stationary distribution of `G` is the PageRank vector:

```text
r = (11/49,13/49,2/7,11/49)^T,       G r = r.
```

The exact order is `3 > 2 > 1 = 4`.

## Story

1. Distinguish a directed arrow's source and destination.
2. Define out-degree and identify vertex 4 as dangling.
3. Encode link following in `H` and expose its zero fourth column.
4. Repair the dangling column by restarting uniformly.
5. Add uniform teleportation to every step.
6. Display the exact positive, column-stochastic Google matrix.
7. Animate two exact iterations from a uniform distribution.
8. Define PageRank as the stationary distribution `Gr=r`.
9. Interpret rank as recursively weighted incoming support plus a teleportation
   baseline.
10. Synthesize direction, repair, and ranking; preview the chapter synthesis.

## Architecture

`DirectedPageRank` is renderer-independent. It validates finite directed graphs,
computes incoming and outgoing neighbors, out-degrees, dangling vertices, the
column-oriented adjacency matrix, raw and repaired link matrices, the uniform
teleportation matrix, the Google matrix, exact iteration trajectories, the
stationary PageRank vector, residuals, total-variation distance, and rank groups.

The scene continues the chapter's established banner, title, heading, color,
spacing, and pacing conventions. Arrowheads make direction explicit, vertex
numerals remain black inside yellow vertices, structural matrices use generous
fraction spacing, standalone entries are aligned with fraction bars, and rank
is visualized with vertex-centered halos.

## Scope boundary

This lesson uses uniform teleportation and the pedagogically convenient value
`alpha=1/2`. It does not claim that PageRank is an objective or universal notion
of importance: the final card states that the ranking depends on both the link
structure and the selected teleportation rule. Personalized teleportation,
weighted directed links, large sparse solvers, and historical search-engine
details are outside this checkpoint.

## Files

```text
engine/directed_page_rank.py
scenes/directed_page_rank_presentation.py
tests/test_directed_page_rank.py
tests/test_directed_page_rank_presentation.py
scripts/check_cp238_directed_page_rank.zsh
scripts/render_cp238_directed_page_rank.zsh
CHECKPOINT_238.md
apply_checkpoint_238.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp238_directed_page_rank.zsh
scripts/render_cp238_directed_page_rank.zsh
```

The render command produces only an uncached low-quality preview for review.
