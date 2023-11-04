lint:
	poetry run flake8 .
	poetry run black --line-length 79 . --check
	poetry run ruff .

format:
	poetry run isort .
	poetry run black --line-length 79 .
	poetry run ruff . --fix

.PHONY: lint format