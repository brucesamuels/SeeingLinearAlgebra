from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
Number=int|float
MatrixData=tuple[tuple[Number,...],...]

def _normalize_matrix(matrix: Iterable[Iterable[Number]]) -> MatrixData:
    rows=tuple(tuple(value for value in row) for row in matrix)
    if not rows: raise ValueError("a matrix must contain at least one row")
    width=len(rows[0])
    if width==0: raise ValueError("a matrix must contain at least one column")
    if any(len(row)!=width for row in rows): raise ValueError("matrix rows must all have the same length")
    return rows

def matrix_shape(matrix):
    m=_normalize_matrix(matrix); return len(m),len(m[0])

def scale_matrix(scalar, matrix):
    m=_normalize_matrix(matrix)
    return tuple(tuple(scalar*v for v in row) for row in m)

def add_matrices(left,right):
    a,b=_normalize_matrix(left),_normalize_matrix(right)
    if matrix_shape(a)!=matrix_shape(b): raise ValueError("matrix addition requires equal dimensions")
    return tuple(tuple(x+y for x,y in zip(ar,br)) for ar,br in zip(a,b))

@dataclass(frozen=True)
class ScalarEntryStep:
    row:int; column:int; scalar:Number; original_value:Number; result:Number


def scalar_entry_steps(scalar,matrix):
    m=_normalize_matrix(matrix); out=[]
    for i,row in enumerate(m):
        for j,v in enumerate(row): out.append(ScalarEntryStep(i,j,scalar,v,scalar*v))
    return tuple(out)

@dataclass(frozen=True)
class MatrixScalarMultiplicationLesson:
    scalar:Number
    matrix:MatrixData
    second_matrix:MatrixData
    negative_scalar:Number
    @property
    def scaled_matrix(self): return scale_matrix(self.scalar,self.matrix)
    @property
    def negative_scaled_matrix(self): return scale_matrix(self.negative_scalar,self.matrix)
    @property
    def distributive_left(self): return scale_matrix(self.scalar,add_matrices(self.matrix,self.second_matrix))
    @property
    def distributive_right(self): return add_matrices(scale_matrix(self.scalar,self.matrix),scale_matrix(self.scalar,self.second_matrix))

MATRIX_SCALAR_MULTIPLICATION_LESSON=MatrixScalarMultiplicationLesson(3,((2,-1),(0,4)),((1,2),(-3,1)),-2)
