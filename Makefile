start:
	poetry run python3 manage.py runserver 8080

install:
	poetry install && poetry run python3 manage.py migrate