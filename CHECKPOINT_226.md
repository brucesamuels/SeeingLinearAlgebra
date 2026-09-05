# Checkpoint 226 — What Is a Graph? Objects, Connections, and Routes

This checkpoint opens **Graphs, Networks, and the Laplacian** by introducing
graph vocabulary visually and from first principles. A graph records which
objects are directly related while ignoring incidental geometric details such
as the lengths, slopes, and shapes of the drawn edges.

## Recurring graph

Use the four-vertex triangle-with-a-tail graph

```text
V = {1,2,3,4}
E = {{1,2},{2,3},{1,3},{3,4}}.
```

Its degrees are `(2,2,3,1)`. It is connected, but removing `{3,4}` separates it
into the connected components `{1,2,3}` and `{4}`. This graph will recur in later
checkpoints for adjacency, walks, incidence, the Laplacian, energy, eigenvectors,
partitioning, and electrical networks.

## Story

1. Begin with four places and direct routes between them.
2. Strip away contextual and geometric detail while preserving the connections.
3. Define vertices, edges, and `G=(V,E)`.
4. Define adjacent vertices and list the neighbors of vertex 3.
5. Define degree and count the four vertex degrees visually.
6. Animate the walk `4,3,1,2,3,1`, allowing repetition and counting five edges.
7. Contrast it with the path `4,3,1,2`, which has no repeated vertex and length 3.
8. Define connectedness by showing that vertex 4 can reach every other vertex.
9. Remove `{3,4}` and reveal two connected components.
10. Close by asking whether zeros and ones can store the same connections.

## Architecture

`SimpleUndirectedGraph` is renderer-independent. It validates a finite simple
undirected graph and provides adjacency, neighbors, degrees, walk and path
validation, walk length, connected components, connectedness, and edge removal.
The Manim scene owns layout, colors, labels, and animation.

## Scope boundary

This checkpoint does not introduce adjacency or degree matrices, matrix
multiplication, orientations, incidence matrices, Laplacians, graph spectra,
weighted or directed graphs, or electrical terminology. Algebraic encoding begins
in the next lesson only after the graph vocabulary is established.

## Files

```text
engine/simple_undirected_graph.py
scenes/graph_vocabulary_presentation.py
tests/test_simple_undirected_graph.py
tests/test_graph_vocabulary_presentation.py
scripts/check_cp226_graph_vocabulary.zsh
scripts/render_cp226_graph_vocabulary.zsh
CHECKPOINT_226.md
apply_checkpoint_226.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp226_graph_vocabulary.zsh
scripts/render_cp226_graph_vocabulary.zsh
```

The render command produces only an uncached low-quality preview for review.
