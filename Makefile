start:
	poetry run python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

dev:
	poetry run python3 manage.py runserver 8080

install:
	poetry install && poetry run python3 manage.py migrate

test:
	poetry run python manage.py test
	poetry run flake8

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

compilemessages:
	poetry run django-admin compilemessages --ignore=.venv

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report