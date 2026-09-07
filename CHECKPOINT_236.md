# Checkpoint 236 — Random Walks and Markov Chains

This checkpoint turns the recurring graph into a simple random walk. At each
step, a walker chooses one neighboring vertex uniformly. The lesson introduces
probability distributions from first principles, encodes one-step movement in
a transition matrix, and connects the stationary distribution back to the
Laplacian null space.

## Convention and numerical spine

Probability distributions are column vectors and evolve by

```text
p_(k+1) = P p_k,       P = A D^(-1).
```

Thus column `j` of `P` records the probabilities of leaving vertex `j`, and
every column sums to one. For the recurring graph,

```text
    [  0  1/2  1/3  0 ]
P = [1/2   0   1/3  0 ]
    [1/2  1/2   0   1 ]
    [  0   0   1/3  0 ].
```

Starting with certainty at vertex 4 gives

```text
p0 = (0,0,0,1)^T
p1 = (0,0,1,0)^T
p2 = (1/3,1/3,0,1/3)^T
p3 = (1/6,1/6,2/3,0)^T
p4 = (11/36,11/36,1/6,2/9)^T.
```

The stationary distribution is proportional to vertex degree:

```text
pi = (1/4,1/4,3/8,1/8)^T,       P pi = pi.
```

Since `P=A D^(-1)`, stationarity gives

```text
L D^(-1) pi = 0,
```

and here `D^(-1) pi=(1/8)1`, returning to the earlier result
`Null(L)=span{1}` for a connected graph.

## Story

1. Define a random walk visually as one uniformly chosen neighboring step.
2. Use vertex degree to determine exact one-step probabilities.
3. Build the column-stochastic transition matrix `P=A D^(-1)` column by column.
4. Introduce a probability distribution as movable mass whose entries are
   nonnegative and sum to one.
5. Animate the first four exact distributions from a point mass at vertex 4.
6. Define and verify a stationary distribution.
7. Explain visually why the stationary weights are proportional to degree.
8. Convert the stationary equation into a Laplacian null-space equation.
9. Synthesize movement, preservation, and equilibrium; preview directed-link
   ranking.

## Architecture

`GraphRandomWalk` is renderer-independent and composes the existing graph,
matrix-encoding, incidence, and Laplacian models. It computes the transition
matrix, validates distributions and step counts, evolves distributions,
generates trajectories, computes the degree-proportional stationary
distribution, verifies stationarity and its Laplacian residual, and measures
total-variation distance.

The scene continues the established banner, title, heading, color, spacing, and
pacing conventions. Structural matrices use extra spacing for fractions,
transition columns are revealed one at a time, probability mass appears as
vertex-centered halos, and vertex numerals remain black inside yellow vertices.

## Scope boundary

This checkpoint treats a simple random walk on an undirected graph with no
isolated vertices. It does not claim that every connected graph converges: the
recurring graph converges because its triangle is an odd cycle, preventing an
endless two-step alternation. Directed links, teleportation, and ranking are
reserved for the next checkpoint.

## Files

```text
engine/graph_random_walk.py
scenes/graph_random_walk_presentation.py
tests/test_graph_random_walk.py
tests/test_graph_random_walk_presentation.py
scripts/check_cp236_graph_random_walk.zsh
scripts/render_cp236_graph_random_walk.zsh
CHECKPOINT_236.md
apply_checkpoint_236.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp236_graph_random_walk.zsh
scripts/render_cp236_graph_random_walk.zsh
```

The render command produces only an uncached low-quality preview for review.

