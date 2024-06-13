start:
	poetry run python3 manage.py runserver

install:
	poetry install && poetry run python3 manage.py migrate