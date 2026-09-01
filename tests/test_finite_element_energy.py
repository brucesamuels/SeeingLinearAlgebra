import numpy as np
import pytest

from engine.finite_element_energy import FiniteElementEnergy1D


def test_default_mesh_and_local_element_data_are_exact():
    model = FiniteElementEnergy1D()
    assert np.allclose(model.nodes, [0, 1 / 3, 2 / 3, 1])
    assert model.element_length == pytest.approx(1 / 3)
    assert np.allclose(model.local_stiffness(), [[3, -3], [-3, 3]])
    assert np.allclose(model.local_load(), [1 / 6, 1 / 6])


def test_assembly_produces_full_and_reduced_stiffness_matrices():
    model = FiniteElementEnergy1D()
    assert np.allclose(
        model.full_stiffness_matrix(),
        [[3, -3, 0, 0], [-3, 6, -3, 0], [0, -3, 6, -3], [0, 0, -3, 3]],
    )
    assert np.allclose(model.stiffness_matrix(), [[6, -3], [-3, 6]])


def test_assembly_produces_full_and_reduced_load_vectors():
    model = FiniteElementEnergy1D()
    assert np.allclose(model.full_load_vector(), [1 / 6, 1 / 3, 1 / 3, 1 / 6])
    assert np.allclose(model.load_vector(), [1 / 3, 1 / 3])


def test_discrete_energy_gradient_gives_the_finite_element_system():
    model = FiniteElementEnergy1D()
    coefficients = np.array([2 / 15, 1 / 10])
    expected = model.stiffness_matrix() @ coefficients - model.load_vector()
    assert np.allclose(model.energy_gradient(coefficients), expected)
    assert model.discrete_energy(coefficients) == pytest.approx(
        0.5 * coefficients @ model.stiffness_matrix() @ coefficients
        - model.load_vector() @ coefficients
    )


def test_solution_is_unique_stationary_point_and_has_expected_nodal_values():
    model = FiniteElementEnergy1D()
    coefficients = model.solve()
    assert np.allclose(coefficients, [1 / 9, 1 / 9])
    assert np.allclose(model.energy_gradient(coefficients), [0, 0])
    assert np.allclose(model.nodal_values(), [0, 1 / 9, 1 / 9, 0])


@pytest.mark.parametrize("coefficients", ([1, 0], [0, 1], [2, -3]))
def test_reduced_stiffness_energy_is_positive(coefficients):
    assert FiniteElementEnergy1D().stiffness_energy(coefficients) > 0


def test_hat_basis_values_have_the_nodal_delta_property():
    model = FiniteElementEnergy1D()
    assert np.allclose(model.basis_values(1, model.nodes), [0, 1, 0, 0])
    assert np.allclose(model.basis_values(2, model.nodes), [0, 0, 1, 0])
    assert model.basis_values(1, 1 / 6) == pytest.approx(0.5)


def test_piecewise_linear_and_exact_solutions_agree_at_interior_nodes():
    model = FiniteElementEnergy1D()
    assert np.allclose(model.approximate_solution(model.nodes), model.nodal_values())
    assert np.allclose(
        model.approximate_solution(model.nodes[1:-1]),
        model.exact_solution(model.nodes[1:-1]),
    )
    assert model.approximate_solution(0.5) == pytest.approx(1 / 9)
    assert model.exact_solution(0.5) == pytest.approx(1 / 8)


@pytest.mark.parametrize("element_count", (1, 2.5))
def test_invalid_element_counts_are_rejected(element_count):
    with pytest.raises(ValueError, match="element_count"):
        FiniteElementEnergy1D(element_count)


def test_invalid_source_is_rejected():
    with pytest.raises(ValueError, match="source"):
        FiniteElementEnergy1D(source=np.inf)


@pytest.mark.parametrize("coefficients", ([1], [1, np.inf]))
def test_invalid_coefficients_are_rejected(coefficients):
    with pytest.raises(ValueError, match="coefficients"):
        FiniteElementEnergy1D().discrete_energy(coefficients)


@pytest.mark.parametrize("interior_index", (0, 3, 1.5))
def test_invalid_basis_indices_are_rejected(interior_index):
    with pytest.raises(ValueError, match="interior_index"):
        FiniteElementEnergy1D().basis_values(interior_index, 0.5)


@pytest.mark.parametrize("point", (-0.1, 1.1, np.inf))
def test_invalid_solution_evaluation_points_are_rejected(point):
    with pytest.raises(ValueError, match="evaluation points"):
        FiniteElementEnergy1D().approximate_solution(point)
