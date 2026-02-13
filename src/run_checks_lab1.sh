#!/bin/bash


poetry run mypy --namespace-packages --explicit-package-bases .
echo ""

poetry run ruff check .
echo ""


poetry run pytest --random-order --alluredir=./allure-results
echo ""


poetry run allure serve ./allure-results