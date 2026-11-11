# Medical Center API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver a functional, tested Django REST API for medical-center scheduling, runnable with Docker Compose and PostgreSQL, with English documentation and deployment-ready configuration.

**Architecture:** Use one Django project with bounded-context-oriented apps: `specialists`, `patients`, `facilities`, `scheduling`, and `appointments`. Use Django ORM, Django REST Framework viewsets/serializers, service-level appointment conflict validation, and logical deactivation for master data.

**Tech Stack:** Python 3.12, Django 5.2, Django REST Framework, PostgreSQL 16, psycopg, drf-spectacular, Docker Compose, pytest, pytest-django.

**Spec:** `docs/specs/2026-11-11-medical-center-api-design.md`

## Global Constraints

- All project-facing names and documentation must be in English.
- PostgreSQL is the only application database backend.
- No credentials or real patient data may be committed.
- Database schema changes must use Django migrations.
- The local stack must run with `docker compose up --build`.
- The API base path is `/api/v1/`.
- Swagger UI is `/api/docs/`; schema is `/api/schema/`.
- Core records use logical deactivation where historical appointments require retention.

## Review Focus

- Appointment interval boundaries: back-to-back appointments are allowed; overlapping intervals are rejected.
- Appointment state transitions: cancelled and completed appointments cannot be silently rescheduled or cancelled again.
- Inactive references: inactive specialists, patients, and offices cannot receive new appointments.
- Schedule boundaries: appointments must fit entirely inside an active working-schedule interval.
- Container startup: the web service must wait for PostgreSQL and apply migrations successfully on a fresh volume.

### Task 1: Repository baseline and Docker/PostgreSQL foundation

**Files:**
- Create: `pyproject.toml`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example`, `docker/entrypoint.sh`
- Modify: `.gitignore`, `README.md`
- Test: `tests/test_container_configuration.py`

**Interfaces:**
- Produces a `web` service on port 8000 and a `db` PostgreSQL service on port 5432.
- Produces environment variables for Django and PostgreSQL with safe defaults only.

- [ ] Write tests asserting required Compose services, ports, healthcheck, persistent volume, and ignored `.env`.
- [ ] Run the configuration tests and verify they fail because the files are absent.
- [ ] Add the minimal Python/Django dependency and Docker configuration.
- [ ] Add an entrypoint that waits for PostgreSQL, runs `migrate`, and starts the development server.
- [ ] Run configuration tests and build the image.

### Task 2: Django project and shared API configuration

**Files:**
- Create: `manage.py`, `config/settings.py`, `config/urls.py`, `config/wsgi.py`, `config/asgi.py`, `config/api.py`
- Create: `tests/test_health.py`

- [ ] Write a health endpoint test expecting HTTP 200 and a JSON status response.
- [ ] Verify the test fails before project configuration exists.
- [ ] Implement environment-based settings, PostgreSQL connection, DRF defaults, pagination, and OpenAPI routes.
- [ ] Run the health test and `python manage.py check` in Docker.

### Task 3: Specialists and patients

**Files:**
- Create: `specialists/{models,serializers,views,urls,admin}.py`, `specialists/migrations/0001_initial.py`
- Create: `patients/{models,serializers,views,urls,admin}.py`, `patients/migrations/0001_initial.py`
- Create: `tests/test_specialists_api.py`, `tests/test_patients_api.py`

- [ ] Write tests for CRUD, search/filtering, uniqueness, required fields, and logical deactivation.
- [ ] Verify the tests fail before models and endpoints exist.
- [ ] Implement `Specialty`, `Specialist`, and `Patient` with timestamps, active flags, and database constraints.
- [ ] Implement serializers and REST endpoints under `/api/v1/`.
- [ ] Generate/apply migrations and run the focused tests.

### Task 4: Facilities and working schedules

**Files:**
- Create: `facilities/{models,serializers,views,urls,admin}.py`, `facilities/migrations/0001_initial.py`
- Create: `scheduling/{models,serializers,views,urls,admin}.py`, `scheduling/migrations/0001_initial.py`
- Create: `tests/test_facilities_api.py`, `tests/test_scheduling_api.py`

- [ ] Write tests for office CRUD/deactivation and schedule interval validation.
- [ ] Verify the tests fail before implementation.
- [ ] Implement `Office` and `WorkingSchedule`, including weekday/time constraints and specialist relationships.
- [ ] Implement endpoints and migrations.
- [ ] Run focused tests and Django system checks.

### Task 5: Appointment use cases and edge cases

**Files:**
- Create: `appointments/{models,serializers,views,urls,services,admin}.py`, `appointments/migrations/0001_initial.py`
- Create: `tests/test_appointments_api.py`

- [ ] Write failing tests for create/list/update/cancel/complete, inactive references, invalid intervals, schedule boundaries, specialist conflicts, office conflicts, back-to-back appointments, and invalid state transitions.
- [ ] Verify the tests fail for missing appointment behavior.
- [ ] Implement `Appointment` and a transaction-safe conflict validation service.
- [ ] Implement status transition validation and filtered list endpoints.
- [ ] Generate/apply migrations and run all appointment tests.

### Task 6: Documentation, user guide, and deployment readiness

**Files:**
- Modify: `README.md`
- Create: `docs/USER_GUIDE.md`, `docs/API_REFERENCE.md`, `docs/DEPLOYMENT.md`
- Create: `.github/workflows/ci.yml`

- [ ] Write documentation checks for required commands, URLs, environment variables, and deployment notes.
- [ ] Document Docker Compose startup, migrations, tests, admin creation, API examples, troubleshooting, backups, and production settings.
- [ ] Document portability to a VM and AWS using environment injection and external PostgreSQL for production.
- [ ] Add CI to install dependencies, run checks, migrations, and tests against PostgreSQL.
- [ ] Run the complete suite in Docker, validate the documented commands, inspect the final diff for secrets and personal paths, and report exact results.
