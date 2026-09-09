# Checkpoint 240 — Graphs, Networks, and the Laplacian: The Big Picture

This checkpoint closes the instructional sequence by synthesizing the graph
chapter rather than introducing another theorem. Its organizing principle is
that the same graph supports several linear-algebraic representations, and the
right matrix is chosen by the question being asked.

## Recurring numerical spine

The triangle-with-a-tail graph remains the sole undirected example. The lesson
reassembles its exact matrices and familiar signal `x=(1,2,3,4)^T`:

```text
A records adjacency,          (A^2)_14 = 1,
B x = (1,1,2,1)^T,            L = B^T B = D-A,
L x = (-3,0,2,1)^T,           x^T L x = 7,
spec(L) = (0,1,3,4),          v2 = (1,1,0,-2)^T.
```

The Fiedler sweep isolates vertex 4 across the bridge with RatioCut `4/3`.
The unit-resistance electrical example retains grounded potentials
`(0,1/3,2/3,5/3)^T` and effective resistance `5/3`. The undirected random walk
has stationary distribution `(1/4,1/4,3/8,1/8)^T`.

The final probability application is explicitly separated from the undirected
spine: directed links, dangling-column repair, and teleportation produce the
PageRank vector `(11/49,13/49,2/7,11/49)^T` and order `3>2>1=4`.

## Story

1. Present adjacency, incidence, Laplacian, and probability matrices as four
   lenses on graph questions.
2. Revisit adjacency and fixed-length walk counting with `A` and `A^k`.
3. Reassemble the vertex-to-edge-to-vertex composition `L=B^T B=D-A`.
4. Join Laplacian energy to incidence subspaces: components, gradients, and
   cycles.
5. Use the incidence dimension formulas to count components and cycles.
6. Review the spectral gap, Fiedler vector, and bridge partition.
7. Review electrical potentials, conserved current, grounding, and effective
   resistance through `Lv=b`.
8. Review degree-normalized random walks and their stationary distribution.
9. Separate the directed PageRank construction into repair, teleportation, and
   a stationary ranking.
10. End with a question-driven recognition guide for choosing `A`, `B`, `L`,
    `P`, or `G`.

## Architecture

`GraphChapterSynthesis` is renderer-independent and composes the approved graph
models rather than reimplementing their algorithms. It exposes the exact
adjacency, degree, incidence, and Laplacian matrices; recurring signal results;
the spectrum and partition; the electrical solution; stationary random-walk
probabilities; PageRank; and a question-to-representation guide.

The Manim scene retains the chapter's banner, title, heading, colors, spacing,
and pacing. Matrices are structural, fractions receive generous vertical
spacing, directed and undirected edges remain visually distinct, and vertex
numerals are black inside yellow vertices.

## Scope boundary

This is a synthesis lesson. It introduces no weighted graphs, normalized
Laplacian theorem, new Markov-chain classification, new partitioning objective,
or new electrical model. The next checkpoint will assemble the complete
chapter preview; the high-definition master remains a separate checkpoint.

## Files

```text
engine/graph_chapter_synthesis.py
scenes/graph_chapter_synthesis_presentation.py
tests/test_graph_chapter_synthesis.py
tests/test_graph_chapter_synthesis_presentation.py
scripts/check_cp240_graph_chapter_synthesis.zsh
scripts/render_cp240_graph_chapter_synthesis.zsh
CHECKPOINT_240.md
apply_checkpoint_240.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp240_graph_chapter_synthesis.zsh
scripts/render_cp240_graph_chapter_synthesis.zsh
```

The render command produces only an uncached low-quality preview for review.
