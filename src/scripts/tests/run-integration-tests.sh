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

echo "=== Integration tests completed ==="