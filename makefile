format:
	@echo "formating"
	poetry run ruff format src

type:
	@echo "typing"
	poetry run mypy src
