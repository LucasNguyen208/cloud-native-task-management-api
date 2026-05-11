#!/bin/bash

FAILED=0

echo "=================================="
echo "Running Black formatter..."
echo "=================================="
black . || FAILED=1

echo "=================================="
echo "Running Black check..."
echo "=================================="
black --check . || FAILED=1

echo ""
echo "=================================="
echo "Running Ruff..."
echo "=================================="
ruff format . || FAILED=1

echo ""
echo "=================================="
echo "Running Ruff..."
echo "=================================="
ruff check . || FAILED=1

echo ""
echo "=================================="
echo "Running Pytest..."
echo "=================================="
pytest -v --tb=short --cov --cov-report=term-missing || FAILED=1

echo ""

if [ $FAILED -eq 0 ]; then
    echo "=================================="
    echo "All checks passed!"
    echo "=================================="
else
    echo "=================================="
    echo "Some checks failed!"
    echo "=================================="
    exit 1
fi
