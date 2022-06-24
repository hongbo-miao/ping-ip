# Setup
setup:
	poetry install

# Run
run-reactive:
	poetry run poe run-reactive
run-multiprocess:
	poetry run poe run-multiprocess

# Test
test:
	poetry run poe test

# Static Type Check
python-static-type-check:
	poetry run poe static-type-check-mypy

# Lint
lint-python-black:
	poetry run poe lint-black
lint-python-black-fix:
	poetry run poe lint-black-fix
lint-python-flake8:
	poetry run poe lint-flake8
lint-python-isort:
	poetry run poe lint-isort
lint-python-isort-fix:
	poetry run poe lint-isort-fix
