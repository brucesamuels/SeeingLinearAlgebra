# Seeing Linear Algebra — Episode 1
## Vectors, Magnitude, Unit Vectors, Coordinates, and Span

This script follows Mr. Samuels' classroom lesson. Timestamps are placeholders until the final preview is approved.

### 00:00 — Brooklyn Tech opening
Welcome to *Seeing Linear Algebra*, from Brooklyn Technical High School. In this first episode, we begin with vectors and build toward one of the central ideas in linear algebra: span.

### 00:15 — Three viewpoints
A physicist usually pictures a vector as an arrow with a direction and a magnitude. A computer scientist often sees an ordered list of numbers. A mathematician works with a more abstract object that can be added to other vectors and multiplied by scalars. Linear algebra moves freely among all three viewpoints.

### 00:55 — Equivalent vectors
A vector does not remember where an arrow was drawn. These arrows begin at different points, but they have the same length and point in the same direction. When we slide them back to the origin, they coincide. Equal vectors have the same magnitude and direction.

### 01:35 — Scalar multiplication
Multiplying a vector by a scalar changes its length. Scalars with magnitude greater than one stretch it. Scalars between negative one and one shrink it. A negative scalar reverses its direction. Multiplying by zero collapses everything to the zero vector.

### 02:25 — Vector addition
To add two vectors, place the tail of the second vector at the tip of the first. The sum is the arrow from the original starting point to the final tip. This tip-to-tail construction is the geometric form of adding corresponding components.

### 03:15 — Magnitude
The magnitude of a vector is its length. For the vector three, negative four, the horizontal and vertical components form a right triangle. The Pythagorean theorem gives a length of five. In n dimensions, the same rule becomes the square root of the sum of the squares of all components.

### 04:20 — Unit vectors
A unit vector has length one. To point in the same direction as a nonzero vector while changing its length to one, divide by its magnitude. The vector three, negative four has magnitude five, so dividing each component by five produces the unit vector three-fifths, negative four-fifths.

### 05:15 — Standard basis and coordinates
The standard basis vectors are unit steps along the coordinate axes. In the plane, e one is one step in the horizontal direction, and e two is one step in the vertical direction. Coordinates are instructions: three, two means take three copies of e one, two copies of e two, and add them.

### 06:25 — Linear combinations
A linear combination is built from the two operations we already know. First scale vectors by numbers. Then add the results. The expression a v plus b w records that entire construction.

### 07:20 — Span in one and two dimensions
The span is the set of every vector obtainable from all possible linear combinations. One nonzero vector has only one independent direction, so its scalar multiples fill a line. Two nonparallel vectors provide two independent directions. By varying both scalars and adding, we can reach the entire plane.

### 08:35 — Higher dimensions
Three independent directions fill three-dimensional space. Beyond three dimensions, visualization fails us, but the algebra does not change. A linear combination in R n still consists of scalar multiples followed by vector addition.

### 09:20 — Closing
Scalar multiplication and vector addition create linear combinations. All linear combinations together form a span. In the next episode, we ask when such a set is a vector subspace and what happens when some vectors are redundant.
