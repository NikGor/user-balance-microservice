.PHONY: install test run

install:
	poetry install

test:
	poetry run python manage.py test

run:
	poetry run python manage.py runserver

lint:
	poetry run flake8 UserBalanceMicroservice

selfcheck:
	poetry check

check: selfcheck test lint

amend-and-push:
	git add .
	git commit --amend --no-edit
	git push --force
