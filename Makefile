install:
	@poetry install

start:
	@poetry run python manage.py runserver

lint:
	@poetry run flake8 task_manager

test:
	@poetry run python manage.py test

test_detail:
	@poetry run python manage.py test --verbosity 2

test_coverage:
	@poetry run coverage run --source='.' manage.py test

test-coverage-report-xml:
	@poetry run coverage xml

selfcheck:
	@poetry check

check: selfcheck lint test

.PHONY: install test lint selfcheck check