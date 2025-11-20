comment ?= ""

format:
	@echo "formating"
	poetry run ruff format src

type:
	@echo "typing"
	poetry run mypy src

run:
	@echo "running app"
	poetry run python src/main.py


add_migration:
	@echo "creae migrtion"
	poetry run alembic revision --autogenerate -m $(comment)


migrate:
	@echo "migrtion head"
	poetry run alembic upgrade head


downgrade:
	@echo "downgrade"
	poetry run alembic downgrade -1  