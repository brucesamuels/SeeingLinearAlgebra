"""Repository-source audit for scalar-multiplication reuse.

The audit inspects existing source and tests without importing Manim or changing
engine behavior. It reports evidence; it does not manufacture a new API.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class AuditFinding:
    key: str
    passed: bool
    evidence: str


@dataclass(frozen=True, slots=True)
class ScalarMultiplicationAudit:
    findings: tuple[AuditFinding, ...]

    @property
    def passed(self) -> bool:
        return all(finding.passed for finding in self.findings)

    @property
    def passed_count(self) -> int:
        return sum(finding.passed for finding in self.findings)

    @property
    def failed_count(self) -> int:
        return len(self.findings) - self.passed_count

    def finding(self, key: str) -> AuditFinding:
        for finding in self.findings:
            if finding.key == key:
                return finding
        raise KeyError(f"unknown audit finding: {key!r}")

    def to_markdown(self) -> str:
        status = "SUPPORTED" if self.passed else "NEEDS REVIEW"
        lines = [
            "# Scalar Multiplication Reuse Audit",
            "",
            f"Overall result: **{status}**",
            "",
            "| Check | Result | Evidence |",
            "|---|---|---|",
        ]
        for finding in self.findings:
            result = "PASS" if finding.passed else "REVIEW"
            evidence = finding.evidence.replace("|", r"\|").replace("\n", " ")
            lines.append(f"| `{finding.key}` | {result} | {evidence} |")
        lines.append("")
        return "\n".join(lines)


def audit_scalar_multiplication_support(repo_root: Path) -> ScalarMultiplicationAudit:
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be a Path")

    engine_dir = repo_root / "engine"
    tests_dir = repo_root / "tests"

    linear_source_paths = tuple(
        path for path in engine_dir.glob("*linear_combination*.py")
        if path.is_file() and "manim" not in path.name
    )
    test_paths = tuple(
        path for path in tests_dir.glob("test*linear_combination*.py")
        if path.is_file()
    )

    findings = (
        _finding_files(linear_source_paths),
        _finding_core_symbols(linear_source_paths),
        _finding_no_two_term_minimum(linear_source_paths),
        _finding_snapshot_contract(linear_source_paths),
        _finding_geometry_generalizes(linear_source_paths),
        _finding_existing_test_evidence(test_paths),
        _finding_renderer_independence(linear_source_paths),
    )
    return ScalarMultiplicationAudit(findings)


def _read(paths: Iterable[Path]) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def _finding_files(paths: tuple[Path, ...]) -> AuditFinding:
    names = ", ".join(path.name for path in paths)
    return AuditFinding(
        "linear_combination_sources",
        bool(paths),
        names or "No renderer-independent linear-combination source found.",
    )


def _finding_core_symbols(paths: tuple[Path, ...]) -> AuditFinding:
    symbols: set[str] = set()
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                symbols.add(node.name)

    required = {"LinearCombination", "CoefficientSweepPath"}
    present = required.intersection(symbols)
    missing = required - symbols
    return AuditFinding(
        "core_pipeline_symbols",
        not missing,
        (
            f"Present: {sorted(present)}"
            if not missing
            else f"Missing: {sorted(missing)}; present: {sorted(present)}"
        ),
    )


def _finding_no_two_term_minimum(paths: tuple[Path, ...]) -> AuditFinding:
    text = _read(paths).lower()
    suspicious = (
        "at least two" in text
        or "minimum of two" in text
        or "term_count < 2" in text
        or "len(vectors) < 2" in text
    )
    return AuditFinding(
        "no_explicit_two_term_minimum",
        not suspicious,
        (
            "No source text imposing a two-term minimum was found."
            if not suspicious
            else "Source contains wording or logic that may impose two terms."
        ),
    )


def _finding_snapshot_contract(paths: tuple[Path, ...]) -> AuditFinding:
    text = _read(paths)
    fields = ("coefficients", "terms", "partial_sums", "result")
    present = tuple(field for field in fields if field in text)
    return AuditFinding(
        "scalar_compatible_snapshot",
        len(present) == len(fields),
        f"Snapshot-related fields found: {present}",
    )


def _finding_geometry_generalizes(paths: tuple[Path, ...]) -> AuditFinding:
    text = _read(paths)
    indicators = (
        "term_count",
        "shape",
        "partial_sums",
        "term_segments",
    )
    present = tuple(indicator for indicator in indicators if indicator in text)
    return AuditFinding(
        "term_count_generalization",
        len(present) >= 2,
        f"Generalization indicators found: {present}",
    )


def _finding_existing_test_evidence(paths: tuple[Path, ...]) -> AuditFinding:
    text = _read(paths).lower()
    indicators = (
        "single",
        "one_term",
        "one term",
        "term_count",
        "shape (1",
        "shape == (1",
    )
    present = tuple(indicator for indicator in indicators if indicator in text)
    return AuditFinding(
        "existing_one_term_test_evidence",
        bool(present),
        (
            f"Possible one-term test indicators: {present}"
            if present
            else "No explicit one-term test evidence found; CP42 should add it."
        ),
    )


def _finding_renderer_independence(paths: tuple[Path, ...]) -> AuditFinding:
    text = _read(paths)
    imports_manim = "import manim" in text or "from manim" in text
    return AuditFinding(
        "renderer_independent_core",
        bool(paths) and not imports_manim,
        (
            "No Manim import found in audited core sources."
            if not imports_manim
            else "A Manim import was found in an audited core source."
        ),
    )
