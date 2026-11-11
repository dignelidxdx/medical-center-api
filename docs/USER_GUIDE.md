# User Guide

## Start the application

1. Start Docker Desktop.
2. Open a terminal in the repository directory.
3. Copy `.env.example` to `.env`.
4. Run `docker compose up --build`.
5. Open Swagger UI at `http://localhost:8000/api/docs/`.

## Recommended data-entry order

1. Create specialties.
2. Create specialists linked to specialties.
3. Create patients.
4. Create offices.
5. Create specialist working schedules.
6. Create appointments.

Appointments are accepted only when the specialist, patient, and office are active, the interval is valid, the appointment fits a working schedule, and neither the specialist nor the office has an overlapping scheduled appointment.

## Troubleshooting

- If port 8000 is busy, change the host side of the web port mapping in `docker-compose.yml`.
- If port 5432 is busy, change `POSTGRES_PORT` in `.env` and the host side of the database port mapping.
- If the database is unavailable, run `docker compose logs db` and then `docker compose up -d` again.
- If migrations are pending, run `docker compose exec web python manage.py migrate`.

