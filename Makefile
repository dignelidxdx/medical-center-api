.PHONY: up down build build-distroless scan scan-distroless logs migrate makemigrations test coverage check shell createsuperuser schema

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

build-distroless:
	docker build -f Dockerfile.distroless -t medical-center-api:distroless .

scan: build
	docker scout cves local://medical-center-api:local

scan-distroless: build-distroless
	docker scout cves local://medical-center-api:distroless

logs:
	docker compose logs -f web

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

test:
	docker compose exec web pytest

coverage:
	docker compose exec web pytest --cov=. --cov-report=term-missing

check:
	docker compose exec web python manage.py check

shell:
	docker compose exec web python manage.py shell

createsuperuser:
	docker compose exec web python manage.py createsuperuser

schema:
	docker compose exec web python manage.py sqlmigrate specialists 0001

