import numpy as np

from engine.subspace_projection import SubspaceProjectionLesson


def test_orthonormal_example_basis_is_orthonormal() -> None:
    lesson = SubspaceProjectionLesson()
    snapshot = lesson.example()
    assert lesson.is_orthonormal(snapshot.basis)


def test_orthonormal_example_projection_is_222() -> None:
    snapshot = SubspaceProjectionLesson().example()
    assert np.allclose(snapshot.projection, np.array([2.0, 2.0, 2.0]))


def test_general_example_basis_is_not_orthonormal() -> None:
    lesson = SubspaceProjectionLesson()
    snapshot = lesson.general_basis_example()
    assert not lesson.is_orthonormal(snapshot.basis)


def test_general_example_gram_matrix_and_inverse_are_clean() -> None:
    snapshot = SubspaceProjectionLesson().general_basis_example()
    assert np.allclose(snapshot.gram_matrix, np.array([[2.0, 2.0], [2.0, 6.0]]))
    assert np.allclose(snapshot.gram_inverse, np.array([[0.75, -0.25], [-0.25, 0.25]]))


def test_general_example_coefficients_are_ones() -> None:
    snapshot = SubspaceProjectionLesson().general_basis_example()
    assert np.allclose(snapshot.rhs, np.array([4.0, 8.0]))
    assert np.allclose(snapshot.coefficients, np.array([1.0, 1.0]))


def test_general_and_orthonormal_bases_give_same_projection() -> None:
    lesson = SubspaceProjectionLesson()
    general = lesson.general_basis_example()
    orthonormal = lesson.example()
    assert np.allclose(general.projection, np.array([2.0, 2.0, 2.0]))
    assert np.allclose(general.projection, orthonormal.projection)
    assert np.allclose(general.projection_matrix, orthonormal.projection_matrix)


def test_generic_basis_formula_projects_example_vector() -> None:
    lesson = SubspaceProjectionLesson()
    snapshot = lesson.general_basis_example()
    projected = lesson.project_with_basis_matrix(snapshot.matrix, snapshot.vector)
    assert np.allclose(projected, snapshot.projection)


def test_residual_is_orthogonal_to_general_basis() -> None:
    lesson = SubspaceProjectionLesson()
    snapshot = lesson.general_basis_example()
    assert lesson.residual_is_orthogonal_to_basis(snapshot)
    assert np.allclose(snapshot.residual, np.array([1.0, -1.0, 0.0]))


def test_projection_matrix_is_symmetric_and_idempotent() -> None:
    p = SubspaceProjectionLesson().general_basis_example().projection_matrix
    assert np.allclose(p.T, p)
    assert np.allclose(p @ p, p)
