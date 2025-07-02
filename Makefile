.PHONY: install test lint format check-format type-check coverage clean

# Install dependencies
install:
	pip install -e .
	pip install -r requirements-dev.txt

# Run tests
TEST_PATH=./
test:
	pytest $(TEST_PATH) -v --cov=shadowfax_flash --cov-report=term-missing

# Run linter
lint:
	flake8 shadowfax_flash tests
	mypy shadowfax_flash tests

# Format code
format:
	black shadowfax_flash tests
	isort shadowfax_flash tests

# Check formatting without making changes
check-format:
	black --check shadowfax_flash tests
	isort --check-only shadowfax_flash tests

# Run type checking
type-check:
	mypy shadowfax_flash tests

# Generate coverage report
coverage:
	pytest --cov=shadowfax_flack --cov-report=html

# Clean up
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

# Run all checks
check: check-format lint type-check test
