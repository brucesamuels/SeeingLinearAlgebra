#!/bin/zsh
set -e
python3 - <<'PY'
from engine.vectors import Vector, BasisVector
from engine.subspaces import Subspace
v = Vector([1,2,3,4])
assert v.dimension == 4
assert BasisVector(4,6).dimension == 6
W = Subspace([Vector([1,0,1,0]), Vector([0,1,0,1])])
assert W.dimension == 2 and W.ambient_dimension == 4
assert W.contains(Vector([3,2,3,2]))
assert W.orthogonal_complement().dimension == 2
print("Session 2 mathematical checks passed.")
PY
