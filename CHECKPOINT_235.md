# Checkpoint 235 — Electrical Networks and Laplacian Systems

This checkpoint interprets the recurring graph as an electrical network with a
unit resistor on every edge. Vertex values become electrical potentials, edge
differences drive currents through Ohm's law, and current conservation at every
vertex becomes the Laplacian system

```text
L v = b.
```

No prior circuit vocabulary is assumed; potential, current, resistance, source,
sink, grounding, power, and effective resistance are introduced visually and
from first principles.

## Numerical spine

Inject one unit of current at vertex 4 and remove one unit at vertex 1:

```text
b = (-1,0,0,1)^T.
```

The entries sum to zero, expressing that total injected current equals total
removed current. Since `L 1=0`, potentials are determined only up to an added
constant. Ground vertex 1 by choosing `v_1=0`. The remaining system is

```text
[ 2 -1  0 ][v_2]   [0]
[-1  3 -1 ][v_3] = [0]
[ 0 -1  1 ][v_4]   [1],
```

with exact solution

```text
v = (0,1/3,2/3,5/3)^T.
```

For unit resistance, current from `i` to `j` is `v_i-v_j`. The physical flows
are

```text
4 -> 3: 1,
3 -> 1: 2/3,
3 -> 2: 1/3,
2 -> 1: 1/3.
```

Thus one unit entering at vertex 4 splits at vertex 3 and recombines at the sink
vertex 1. The energy and power identities are

```text
sum I_e^2 R_e = v^T L v = b^T v = 5/3.
```

With unit current, the source-to-sink voltage difference is also the effective
resistance:

```text
R_eff(4,1) = (v_4-v_1)/1 = 5/3.
```

## Story

1. Turn each graph edge into a unit resistor and introduce potential and current.
2. Apply Ohm's law to edge `4 -> 3` using the exact potentials.
3. Introduce current conservation at vertex 3 and connect its local equation to
   one Laplacian coordinate.
4. Assemble all vertex equations structurally as `L v=b` and explain why the
   injection vector must sum to zero.
5. Interpret the Laplacian null space as gauge freedom and ground vertex 1.
6. Solve the grounded three-by-three system for the exact potentials.
7. Animate the four exact currents from source through the network to sink.
8. Identify Laplacian energy with dissipated and supplied power, then compute
   effective resistance.
9. Synthesize the edge law, vertex law, and energy; preview probabilistic
   movement on graphs.

## Architecture

`ElectricalNetworkLaplacian` is renderer-independent and composes the existing
graph, incidence, Laplacian, and energy models. It computes oriented and
endpoint currents, net vertex outflow, injection compatibility, grounded
solutions, source-sink solutions, gauge shifts, dissipated and supplied power,
energy balance, and effective resistance.

The scene continues the established chapter banner, title, heading, color,
spacing, and pacing conventions. Matrices are structural, fractions are given
extra vertical spacing, electrical flows use prominent arrows and flashes, and
vertex numerals remain black inside colored vertices.

## Scope boundary

This checkpoint uses only identical unit resistors on a connected undirected
graph. It does not yet introduce weighted Laplacians, pseudoinverses, multiple
simultaneous sources, AC circuits, or probabilistic transitions. Random walks
and Markov chains begin in CP236.

## Files

```text
engine/electrical_network_laplacian.py
scenes/electrical_network_laplacian_presentation.py
tests/test_electrical_network_laplacian.py
tests/test_electrical_network_laplacian_presentation.py
scripts/check_cp235_electrical_network_laplacian.zsh
scripts/render_cp235_electrical_network_laplacian.zsh
CHECKPOINT_235.md
apply_checkpoint_235.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp235_electrical_network_laplacian.zsh
scripts/render_cp235_electrical_network_laplacian.zsh
```

The render command produces only an uncached low-quality preview for review.
