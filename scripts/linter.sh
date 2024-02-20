poetry run flake8 src tests
poetry run black --check src tests
poetry run isort --check-only src tests
