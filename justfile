default:
    @just --list

# run linter and fix errors
lint:
    @uv run ruff check --preview . --fix

# run linter
lint-check:
    @uv run ruff check --preview .

# Run formatter and fix errors
format:
    @uv run ruff format .

# Check that your code is properly formatted
format-check:
    @uv run ruff format --check .

# Run type checker
typecheck:
    @uv run ty check .

# Run all tests
test:
    @uv run pytest -vvx .

# Run tests with coverage and print report
coverage report_type="html":
    @uv run coverage run -m pytest .
    @uv run coverage report -m
    @uv run coverage {{report_type}}

# Format & lint code
cleanup: lint format

# Run all checks (lint, format, test)
validate: lint-check format-check test

# Lock dependencies
lock:
    @uv lock

# Install dependencies
setup level="dev":
    @uv sync --locked --group={{level}}

# Check for dependency vulnerabilities
deps-security:
    @uv export --format requirements.txt > requirements.txt
    @uv run pip-audit -r requirements.txt

# Check for code vulnerabilities
code-security:
    @uv run bandit -r pydoku

# Check for dead code
dead-code:
    @uv run vulture --min-confidence 80 pydoku/ tests/