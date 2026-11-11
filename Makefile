.PHONY: up down build logs migrate makemigrations test check shell createsuperuser schema

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f web

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose exec web pytest

check:
	docker compose exec web python manage.py check

shell:
	docker compose exec web python manage.py shell

createsuperuser:
	docker compose exec web python manage.py createsuperuser

schema:
	docker compose exec web python manage.py sqlmigrate specialists 0001

