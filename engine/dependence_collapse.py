"""Renderer-independent mathematics for dependence as loss of direction."""
from __future__ import annotations
from dataclasses import dataclass
from numbers import Real
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]

def _readonly(values: ArrayLike) -> FloatArray:
    a = np.asarray(values, dtype=float).copy(); a.setflags(write=False); return a

def _progress(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real): raise TypeError("progress must be real")
    p=float(value)
    if not np.isfinite(p) or not 0 <= p <= 1: raise ValueError("progress must lie in [0, 1]")
    return p

@dataclass(frozen=True)
class DependenceCollapseSnapshot:
    progress: float
    generator_u: FloatArray
    generator_v: FloatArray
    parallelogram_corners: FloatArray
    determinant: float
    area_ratio: float
    rank: int
    dependent_multiplier: float

class DependenceCollapse:
    """Rotate a second 2D generator continuously into a multiple of the first."""
    def __init__(self, generator_u: ArrayLike, initial_v: ArrayLike) -> None:
        u=np.asarray(generator_u,dtype=float); v=np.asarray(initial_v,dtype=float)
        if u.shape != (2,) or v.shape != (2,): raise ValueError("generators must be 2D vectors")
        if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)): raise ValueError("coordinates must be finite")
        if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0: raise ValueError("generators must be nonzero")
        if abs(np.linalg.det(np.column_stack((u,v)))) < 1e-10: raise ValueError("initial generators must be independent")
        self._u=_readonly(u); self._v0=_readonly(v)
        self._theta0=float(np.arctan2(v[1],v[0])); self._theta1=float(np.arctan2(u[1],u[0]))
        delta=(self._theta1-self._theta0+np.pi)%(2*np.pi)-np.pi
        self._delta=float(delta); self._vnorm=float(np.linalg.norm(v)); self._unorm=float(np.linalg.norm(u))
        self._initial_det=abs(float(np.linalg.det(np.column_stack((u,v)))))

    def snapshot(self, progress: Real) -> DependenceCollapseSnapshot:
        p=_progress(progress); theta=self._theta0+p*self._delta
        v=self._vnorm*np.array([np.cos(theta),np.sin(theta)])
        det=float(np.linalg.det(np.column_stack((self._u,v))))
        corners=np.array([[0,0],self._u,self._u+v,v],dtype=float)
        rank=int(np.linalg.matrix_rank(np.column_stack((self._u,v)),tol=1e-10))
        return DependenceCollapseSnapshot(p,_readonly(self._u),_readonly(v),_readonly(corners),det,abs(det)/self._initial_det,rank,self._vnorm/self._unorm)

    def endpoints_for(self, progress: Real, coefficient_pairs: ArrayLike) -> FloatArray:
        pairs=np.asarray(coefficient_pairs,dtype=float)
        if pairs.ndim != 2 or pairs.shape[1] != 2: raise ValueError("coefficient_pairs must have shape (n, 2)")
        if not np.all(np.isfinite(pairs)): raise ValueError("coefficient pairs must be finite")
        s=self.snapshot(progress)
        return _readonly(pairs[:,:1]*s.generator_u + pairs[:,1:]*s.generator_v)
