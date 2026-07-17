from __future__ import annotations

from pathlib import Path

import pytest

from engine.scalar_multiplication_audit import (
    AuditFinding,
    ScalarMultiplicationAudit,
    audit_scalar_multiplication_support,
)


def write_repo(tmp_path: Path, *, explicit_one_term_test: bool = True) -> Path:
    engine = tmp_path / "engine"
    tests = tmp_path / "tests"
    engine.mkdir()
    tests.mkdir()

    (engine / "linear_combination.py").write_text(
        """
class LinearCombinationSnapshot:
    coefficients = None
    terms = None
    partial_sums = None
    result = None

class LinearCombination:
    def snapshot(self, coefficients):
        term_count = len(coefficients)
        return term_count

class CoefficientSweepPath:
    pass
""",
        encoding="utf-8",
    )
    (engine / "linear_combination_geometry.py").write_text(
        """
def geometry(snapshot):
    term_segments = snapshot.partial_sums
    return term_segments
""",
        encoding="utf-8",
    )
    test_text = (
        "def test_one_term():\n    assert term_count == 1\n"
        if explicit_one_term_test
        else "def test_general():\n    assert True\n"
    )
    (tests / "test_linear_combination.py").write_text(
        test_text,
        encoding="utf-8",
    )
    return tmp_path


def test_audit_passes_complete_synthetic_evidence(tmp_path: Path) -> None:
    audit = audit_scalar_multiplication_support(write_repo(tmp_path))

    assert audit.passed
    assert audit.failed_count == 0
    assert audit.finding("core_pipeline_symbols").passed
    assert audit.finding("existing_one_term_test_evidence").passed


def test_audit_marks_missing_one_term_test_for_review(tmp_path: Path) -> None:
    audit = audit_scalar_multiplication_support(
        write_repo(tmp_path, explicit_one_term_test=False)
    )

    assert not audit.passed
    assert not audit.finding("existing_one_term_test_evidence").passed
    assert "CP42" in audit.finding(
        "existing_one_term_test_evidence"
    ).evidence


def test_audit_detects_explicit_two_term_minimum(tmp_path: Path) -> None:
    repo = write_repo(tmp_path)
    path = repo / "engine/linear_combination.py"
    path.write_text(
        path.read_text(encoding="utf-8")
        + '\nERROR = "at least two vectors are required"\n',
        encoding="utf-8",
    )

    audit = audit_scalar_multiplication_support(repo)

    assert not audit.finding("no_explicit_two_term_minimum").passed


def test_markdown_report_is_deterministic() -> None:
    audit = ScalarMultiplicationAudit(
        (
            AuditFinding("first", True, "evidence"),
            AuditFinding("second", False, "review"),
        )
    )

    assert audit.to_markdown() == (
        "# Scalar Multiplication Reuse Audit\n"
        "\n"
        "Overall result: **NEEDS REVIEW**\n"
        "\n"
        "| Check | Result | Evidence |\n"
        "|---|---|---|\n"
        "| `first` | PASS | evidence |\n"
        "| `second` | REVIEW | review |\n"
    )


def test_unknown_finding_raises_key_error() -> None:
    audit = ScalarMultiplicationAudit(
        (AuditFinding("known", True, "evidence"),)
    )

    with pytest.raises(KeyError, match="unknown audit finding"):
        audit.finding("missing")


def test_audit_requires_path() -> None:
    with pytest.raises(TypeError, match="Path"):
        audit_scalar_multiplication_support(".")  # type: ignore[arg-type]
