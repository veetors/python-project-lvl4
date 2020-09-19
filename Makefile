install:
	@poetry install

start:
	@poetry run python manage.py runserver

lint:
	@poetry run flake8 task_manager

ptw:
	@poetry run ptw

test:
	@poetry run pytest --cov=page_loader --cov-report xml tests/

selfcheck:
	@poetry check

check: selfcheck lint test

.PHONY: install test lint selfcheck check