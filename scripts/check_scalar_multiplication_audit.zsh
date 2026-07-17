#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python scripts/audit_scalar_multiplication.py

python -m pytest -q \
  tests/test_scalar_multiplication_audit.py \
  tests/test_audit_scalar_multiplication_script.py

python -m pytest -q

print
print "Audit report:"
print "  $REPO_ROOT/SCALAR_MULTIPLICATION_AUDIT.md"
