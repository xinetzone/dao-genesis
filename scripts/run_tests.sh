#!/usr/bin/env bash
# run_tests.sh
# 用于本地或 CI 环境中执行单元测试和数据校验

set -e

echo "=== Running Python Unit Tests ==="
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Please install it first (e.g. pip install pytest)"
    exit 1
fi
pytest tests/ -v

echo ""
echo "=== Validating Existing Memory Records ==="
python scripts/validate_reviews.py

echo ""
echo "All checks passed successfully!"
