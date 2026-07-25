"""Thin Manim adapter for dependence collapse."""
from __future__ import annotations
from collections.abc import Callable, Mapping
from typing import Any
import numpy as np
from manim import Arrow, Dot, Polygon, VGroup
from engine.dependence_collapse import DependenceCollapseSnapshot

PointMapper=Callable[[np.ndarray],np.ndarray]

class ManimDependenceCollapse:
    def __init__(self, snapshot: DependenceCollapseSnapshot, point_mapper: PointMapper, endpoints: np.ndarray, *, u_kwargs: Mapping[str,Any]|None=None, v_kwargs: Mapping[str,Any]|None=None, polygon_kwargs: Mapping[str,Any]|None=None, dot_kwargs: Mapping[str,Any]|None=None) -> None:
        self._map=point_mapper
        o=self._p(np.zeros(2)); u=self._p(snapshot.generator_u); v=self._p(snapshot.generator_v)
        self.u_arrow=Arrow(o,u,buff=0,**dict(u_kwargs or {})); self.v_arrow=Arrow(o,v,buff=0,**dict(v_kwargs or {}))
        self.parallelogram=Polygon(*(self._p(c) for c in snapshot.parallelogram_corners),**dict(polygon_kwargs or {}))
        self.endpoint_dots=VGroup(*(Dot(self._p(e),**dict(dot_kwargs or {})) for e in endpoints))
        self.mobject=VGroup(self.parallelogram,self.endpoint_dots,self.u_arrow,self.v_arrow)
    def update(self, snapshot: DependenceCollapseSnapshot, endpoints: np.ndarray) -> None:
        o=self._p(np.zeros(2)); self.u_arrow.put_start_and_end_on(o,self._p(snapshot.generator_u)); self.v_arrow.put_start_and_end_on(o,self._p(snapshot.generator_v))
        self.parallelogram.set_points_as_corners([*(self._p(c) for c in snapshot.parallelogram_corners),self._p(snapshot.parallelogram_corners[0])])
        if len(endpoints)!=len(self.endpoint_dots): raise ValueError("endpoint count cannot change")
        for dot,e in zip(self.endpoint_dots,endpoints): dot.move_to(self._p(e))
    def _p(self,x: np.ndarray)->np.ndarray:
        p=np.asarray(self._map(np.asarray(x,dtype=float)),dtype=float)
        if p.shape!=(3,) or not np.all(np.isfinite(p)): raise ValueError("point_mapper must return finite 3D points")
        return p
