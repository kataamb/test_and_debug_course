#!/bin/bash
set -e

echo "=== Running integration tests ==="

# Ждем готовности БД
until pg_isready -h postgres_test -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

# Запускаем тесты
poetry run pytest tests/integration/ -v \
  --junitxml=test-results/integration-tests.xml \
  --cov=src \
  --cov-report=xml:coverage-reports/integration-coverage.xml \
  --cov-report=html:coverage-reports/html \
  --alluredir=test-results/allure-results

# ========== ДИАГНОСТИКА ==========
echo "=== DIAGNOSTICS: Looking for generated files ==="

# Где мы сейчас?
echo "Current directory: $(pwd)"
echo "Listing current directory:"
ls -la

# Проверяем test-results
echo "Checking test-results in current dir:"
ls -la test-results/ 2>/dev/null || echo "No test-results/ in current dir"

# Проверяем /app/test-results
echo "Checking /app/test-results:"
ls -la /app/test-results/ 2>/dev/null || echo "No /app/test-results"

# Проверяем /app/src/test-results
echo "Checking /app/src/test-results:"
ls -la /app/src/test-results/ 2>/dev/null || echo "No /app/src/test-results"

# Проверяем coverage
echo "Checking coverage-reports:"
ls -la coverage-reports/ 2>/dev/null || echo "No coverage-reports/"

echo "=== DIAGNOSTICS END ==="
# ==================================

echo "=== Integration tests completed ==="