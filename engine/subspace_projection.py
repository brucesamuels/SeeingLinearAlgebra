"""Renderer-independent mathematics for CP155: Projection onto a Subspace."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SubspaceProjectionSnapshot:
    """Numerical data for a projection using an orthonormal basis."""

    vector: np.ndarray
    basis: tuple[np.ndarray, ...]
    coefficients: np.ndarray
    projection: np.ndarray
    residual: np.ndarray
    projection_matrix: np.ndarray


@dataclass(frozen=True)
class GeneralBasisProjectionSnapshot:
    """Numerical data for projection using a non-orthonormal basis matrix."""

    vector: np.ndarray
    basis: tuple[np.ndarray, ...]
    matrix: np.ndarray
    gram_matrix: np.ndarray
    gram_inverse: np.ndarray
    rhs: np.ndarray
    coefficients: np.ndarray
    projection: np.ndarray
    residual: np.ndarray
    projection_matrix: np.ndarray


class SubspaceProjectionLesson:
    """Own the mathematics used by the CP155 presentation."""

    LINE_FORMULA = (
        r"\operatorname{proj}_{\mathbf a}\mathbf{x}="
        r"\mathbf a\,\frac{\mathbf a^T\mathbf x}{\mathbf a^T\mathbf a}"
    )
    GENERAL_MATRIX_FORMULA = (
        r"\operatorname{proj}_W\mathbf{x}="
        r"A(A^TA)^{-1}A^T\mathbf{x}"
    )
    NORMAL_EQUATIONS = r"A^TA\mathbf c=A^T\mathbf x"
    ORTHONORMAL_SUM_FORMULA = (
        r"\operatorname{proj}_W\mathbf{x}="
        r"\sum_{i=1}^{k}(\mathbf{q}_i\cdot\mathbf{x})\mathbf{q}_i"
    )
    MATRIX_FORMULA = r"\operatorname{proj}_W\mathbf{x}=QQ^T\mathbf{x}"
    PROJECTION_MATRIX = r"P_W=QQ^T"
    GENERAL_PROJECTION_MATRIX = r"P_W=A(A^TA)^{-1}A^T"
    RESIDUAL_STATEMENT = r"\mathbf{r}=\mathbf{x}-\mathbf{p}\in W^\perp"

    def example(self) -> SubspaceProjectionSnapshot:
        q1 = np.array([1.0, 1.0, 0.0]) / np.sqrt(2.0)
        q2 = np.array([0.0, 0.0, 1.0])
        x = np.array([3.0, 1.0, 2.0])
        q = np.column_stack((q1, q2))
        coefficients = q.T @ x
        projection = q @ coefficients
        residual = x - projection
        projection_matrix = q @ q.T
        return SubspaceProjectionSnapshot(
            vector=x,
            basis=(q1, q2),
            coefficients=coefficients,
            projection=projection,
            residual=residual,
            projection_matrix=projection_matrix,
        )

    def general_basis_example(self) -> GeneralBasisProjectionSnapshot:
        """A clean non-orthonormal basis for the same plane x=y."""

        a1 = np.array([1.0, 1.0, 0.0])
        a2 = np.array([1.0, 1.0, 2.0])
        x = np.array([3.0, 1.0, 2.0])
        a = np.column_stack((a1, a2))
        gram_matrix = a.T @ a
        gram_inverse = np.linalg.inv(gram_matrix)
        rhs = a.T @ x
        coefficients = gram_inverse @ rhs
        projection = a @ coefficients
        residual = x - projection
        projection_matrix = a @ gram_inverse @ a.T
        return GeneralBasisProjectionSnapshot(
            vector=x,
            basis=(a1, a2),
            matrix=a,
            gram_matrix=gram_matrix,
            gram_inverse=gram_inverse,
            rhs=rhs,
            coefficients=coefficients,
            projection=projection,
            residual=residual,
            projection_matrix=projection_matrix,
        )

    @staticmethod
    def project_with_basis_matrix(a: np.ndarray, x: np.ndarray) -> np.ndarray:
        gram = a.T @ a
        return a @ np.linalg.solve(gram, a.T @ x)

    @staticmethod
    def is_orthonormal(basis: tuple[np.ndarray, ...], *, atol: float = 1e-10) -> bool:
        q = np.column_stack(basis)
        return bool(np.allclose(q.T @ q, np.eye(len(basis)), atol=atol))

    @staticmethod
    def residual_is_orthogonal_to_basis(
        snapshot: SubspaceProjectionSnapshot | GeneralBasisProjectionSnapshot,
        *,
        atol: float = 1e-10,
    ) -> bool:
        return all(abs(float(v @ snapshot.residual)) <= atol for v in snapshot.basis)
