import numpy as np
import pytest
from engine.dependence_collapse import DependenceCollapse

def test_collapse_starts_independent_and_ends_dependent():
    m=DependenceCollapse([2.2,0.55],[-0.45,1.8])
    assert m.snapshot(0).rank==2
    assert m.snapshot(1).rank==1
    assert m.snapshot(1).area_ratio==pytest.approx(0,abs=1e-12)

def test_final_generator_is_positive_multiple_of_u():
    m=DependenceCollapse([2.2,0.55],[-0.45,1.8]); s=m.snapshot(1)
    np.testing.assert_allclose(s.generator_v,s.dependent_multiplier*s.generator_u,atol=1e-12)

def test_area_decreases_near_collapse():
    m=DependenceCollapse([2.2,0.55],[-0.45,1.8])
    assert m.snapshot(0).area_ratio > m.snapshot(.5).area_ratio > m.snapshot(.9).area_ratio

def test_endpoint_cloud_collapses_to_rank_one():
    m=DependenceCollapse([2.2,0.55],[-0.45,1.8]); pairs=np.array([(a,b) for a in [-1,0,1] for b in [-1,0,1]])
    endpoints=m.endpoints_for(1,pairs); u=m.snapshot(1).generator_u
    assert all(abs(np.linalg.det(np.column_stack((u,p))))<1e-10 for p in endpoints)

def test_progress_validation():
    m=DependenceCollapse([1,0],[0,1])
    with pytest.raises(ValueError): m.snapshot(1.1)
