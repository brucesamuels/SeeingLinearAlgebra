# Checkpoint 241 — Graphs, Networks, and the Laplacian Preview Assembly

This checkpoint creates the unnumbered chapter title card and assembles a fresh
low-quality preview of the completed **Graphs, Networks, and the Laplacian**
chapter.

## Preview order

1. Graphs, Networks, and the Laplacian title card
2. CP226 — What Is a Graph? Objects, Connections, and Routes
3. CP227 — Adjacency and Degree Matrices: From Picture to Array
4. CP228 — Matrix Powers Count Walks
5. CP229 — The Incidence Matrix: Edges Meet Vertices
6. CP230 — The Graph Laplacian: Differences Return
7. CP231 — Laplacian Energy: Variation Across Edges
8. CP232 — Connected Components and the Laplacian Null Space
9. CP233 — Laplacian Eigenvalues and the Spectral Gap
10. CP234 — The Fiedler Vector and Spectral Partitioning
11. CP235 — Electrical Networks and Laplacian Systems
12. CP236 — Random Walks and Markov Chains
13. CP237 — Long-Term Probabilities and Steady States
14. CP238 — Directed Graphs and PageRank
15. CP239 — The Fundamental Subspaces of a Graph
16. CP240 — Graphs, Networks, and the Laplacian: The Big Picture

The probability lessons remain in their approved progression: an undirected
random walk, a separate development of long-term Markov behavior, and then a
directed-link ranking application. CP239 returns to the incidence subspaces
before CP240 assembles all chapter viewpoints.

## Build behavior

The builder:

1. Requires Python 3.12, Manim Community 0.21.0, ffmpeg, and ffprobe.
2. Detects and verifies the expected scene class in every source file.
3. Renders the title and all fifteen lessons fresh at `480p15` by default.
4. Verifies codec, dimensions, pixel format, and frame-rate compatibility.
5. Concatenates by stream copy without recompressing approved frames.
6. Verifies that the assembled duration matches the sum of its source clips.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp241_graph_chapter_preview.zsh
scripts/render_cp241_graph_chapter_preview.zsh
```

Default output:

```text
media/videos/graphs_networks_laplacian_assembly/GraphsNetworksLaplacian_preview.mp4
```

This is a review assembly, not the final high-definition master. Review the
complete chapter for transitions, pacing, terminology, visual consistency, and
the placement of the probability branch before creating the final checkpoint.
