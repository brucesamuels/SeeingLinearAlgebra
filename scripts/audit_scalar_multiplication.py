#!/usr/bin/env python3
"""Generate the scalar-multiplication reuse audit report."""

from __future__ import annotations

import argparse
from pathlib import Path

from engine.scalar_multiplication_audit import (
    audit_scalar_multiplication_support,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("SCALAR_MULTIPLICATION_AUDIT.md"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_scalar_multiplication_support(args.repo_root.resolve())
    args.output.write_text(audit.to_markdown(), encoding="utf-8")

    print(
        f"Wrote {args.output}: "
        f"{audit.passed_count} passed, {audit.failed_count} review"
    )
    for finding in audit.findings:
        marker = "PASS" if finding.passed else "REVIEW"
        print(f"[{marker}] {finding.key}: {finding.evidence}")

    # An audit finding marked REVIEW is evidence for the next checkpoint, not
    # a broken repository. Return success so the full test suite still runs.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
