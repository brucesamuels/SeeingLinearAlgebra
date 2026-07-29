# Chapter 2 Narration Script — Vector Spaces and Subspaces

## Opening

A collection of vectors can contain many elements without containing many genuinely new directions. In this chapter, we will learn how to recognize the structure hidden inside such collections.

We will ask two related questions: What makes a collection of vectors into a space? And how can a matrix reveal the structure of that space?

## From Dependence to Subspaces

Begin with vectors in three-dimensional space. When the vectors are independent, they can reach throughout the space. But when one vector becomes a linear combination of the others, it adds no new direction. The three-dimensional structure collapses into a plane, and with further dependence it can collapse again into a line.

This leads to the idea of a subspace: a smaller space living inside a larger one, while still obeying the same rules of vector addition and scalar multiplication.

To test whether a set is a subspace, we ask whether it contains the zero vector and whether it remains closed under addition and scalar multiplication. If any one of these conditions fails, the set is not a subspace.

## Basis and Dimension

A spanning set may contain redundant vectors. A basis removes that redundancy while preserving every direction in the space.

A basis is therefore a set of vectors that is both independent and spanning. The number of vectors in a basis is the dimension of the space.

Dimension does not count how many vectors we happen to display. It counts how many independent directions are needed to describe the entire space.

## The Spaces Inside a Matrix

The columns of a matrix span its column space. This is the set of all outputs the matrix can produce.

The null space contains the input vectors that the matrix sends to zero. These are the directions that disappear under the transformation.

The row space contains the independent directions detected by the equations of the matrix. Row reduction changes the rows, but it preserves the row space.

Pivot positions in the reduced matrix identify the corresponding columns of the original matrix that form a basis for the column space. Nonpivot columns add no new direction; they are combinations of the pivot columns.

## Rank and Nullity

When a vector is a linear combination of other vectors, it adds no new dimension. Row reduction reveals the pivot directions that survive and the free directions associated with the null space.

Rank counts the independent directions that survive. Nullity counts the independent directions that collapse to zero. Together, they account for every input dimension.

For a matrix with n columns, rank plus nullity equals n.

## The Four Fundamental Subspaces

A matrix connects an input space to an output space.

Inside the input space, the row space is perpendicular to the null space. Together they fill the entire input space.

Inside the output space, the column space is perpendicular to the left null space. Together they fill the entire output space.

The matrix detects the row space, loses the null space, and produces the column space. The left null space contains the output directions that the matrix cannot reach.

The row space and column space have the same dimension: the rank of the matrix. The null space has dimension n minus the rank, and the left null space has dimension m minus the rank.

## Closing Reflection

A matrix is more than an array of numbers. It organizes directions into what survives, what disappears, what can be produced, and what remains unreachable.

The ideas of basis, dimension, rank, nullity, and the four fundamental subspaces give us a structural view of linear algebra. In the next chapter, we will shift our attention from the spaces themselves to the actions that move vectors from one space to another: linear transformations.
