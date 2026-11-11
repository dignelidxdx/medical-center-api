# Medical Center API Design

## Intent

Build a small, public, educational Django REST API for managing the core operations of a medical consultation center. The project should be easy to run locally with Docker Compose and PostgreSQL, while remaining structured enough to demonstrate domain-oriented Django organization and spec-driven development.

## Goals

- Manage medical specialties and specialists.
- Manage patients.
- Manage consultation offices.
- Manage specialist working schedules.
- Create, list, update, cancel, and logically deactivate appointments.
- Prevent overlapping appointments for the same specialist or office.
- Persist application data in PostgreSQL.
- Apply database schema changes through Django migrations.
- Provide interactive OpenAPI documentation.
- Provide reproducible local setup through Docker Compose.
- Document setup, environment variables, migrations, tests, and API usage in English.

## Non-goals for the MVP

- Online payments.
- Medical records or clinical notes.
- Prescriptions.
- Email or SMS notifications.
- Multi-branch organizations.
- Patient self-registration.
- Production deployment configuration.
- Complex role-based authorization.

## Proposed approach

Use Django REST Framework organized by bounded-context-oriented Django applications, without introducing a repository pattern or a separate domain framework. This keeps the project simple enough to learn while avoiding one large application containing every model and endpoint.

The initial applications are:

- `specialists`: specialists and specialties.
- `patients`: patient records.
- `facilities`: consultation offices.
- `scheduling`: working schedules and availability rules.
- `appointments`: appointment lifecycle and conflict validation.

## Bounded contexts

### Specialists

Owns medical specialists and medical specialties. A specialist belongs to one specialty in the MVP.

### Patients

Owns patient identity and contact information. Clinical history is explicitly out of scope.

### Facilities

Owns consultation offices and their active/inactive status.

### Scheduling

Owns recurring working-hour definitions for specialists. It does not create appointments directly.

### Appointments

Owns appointment booking, status changes, cancellation, and conflict checks. It references specialists, patients, and offices by foreign key.

## Core use cases

### Specialty management

- Create a specialty.
- List active specialties.
- Update a specialty.
- Deactivate a specialty.

### Specialist management

- Create a specialist associated with a specialty.
- List and filter specialists.
- Update specialist contact or specialty information.
- Deactivate a specialist without deleting historical appointments.

### Patient management

- Create a patient.
- List and search patients.
- Update patient contact information.
- Deactivate a patient without deleting historical appointments.

### Facility management

- Create a consultation office.
- List available offices.
- Update office information.
- Deactivate an office.

### Scheduling management

- Define a specialist's weekly working schedule.
- Update or deactivate a schedule entry.
- Validate that an appointment falls within a specialist's working schedule.

### Appointment management

- Create an appointment.
- List appointments with filters by date, specialist, patient, office, and status.
- Reschedule an appointment.
- Cancel an appointment.
- Mark an appointment as completed.
- Reject appointments that overlap for the same specialist or office.

## Proposed data model

### Specialty

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

### Specialist

- `id`
- `first_name`
- `last_name`
- `license_number`
- `email`
- `phone`
- `specialty_id`
- `is_active`
- `created_at`
- `updated_at`

### Patient

- `id`
- `first_name`
- `last_name`
- `document_number`
- `date_of_birth`
- `email`
- `phone`
- `is_active`
- `created_at`
- `updated_at`

### Office

- `id`
- `name`
- `floor`
- `description`
- `is_active`
- `created_at`
- `updated_at`

### WorkingSchedule

- `id`
- `specialist_id`
- `weekday`
- `start_time`
- `end_time`
- `is_active`
- `created_at`
- `updated_at`

### Appointment

- `id`
- `specialist_id`
- `patient_id`
- `office_id`
- `start_at`
- `end_at`
- `status`
- `reason`
- `notes`
- `created_at`
- `updated_at`

Appointment statuses will initially be `scheduled`, `cancelled`, and `completed`.

## API conventions

- Base path: `/api/v1/`.
- Resource names use plural nouns: `/specialists/`, `/patients/`, `/appointments/`.
- JSON request and response bodies.
- Standard HTTP status codes.
- Pagination for list endpoints.
- Filtering for appointment lists.
- OpenAPI schema at `/api/schema/`.
- Swagger UI at `/api/docs/`.

## Local infrastructure

Docker Compose will define:

- `web`: Django development server.
- `db`: PostgreSQL database with a persistent named volume.

The `web` container will use an entrypoint that waits for PostgreSQL, applies migrations, and starts Django. Credentials will come from an ignored `.env` file created from `.env.example`.

Expected local commands:

```bash
docker compose up --build
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
```

Expected local URLs:

- API: `http://localhost:8000/api/v1/`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
- PostgreSQL: `localhost:5432`

## Dependencies

- Django
- djangorestframework
- drf-spectacular
- psycopg[binary]
- python-dotenv or an equivalent environment configuration package
- pytest
- pytest-django

## Security and privacy constraints

- No credentials committed to the repository.
- `.env` remains ignored; `.env.example` contains safe placeholders only.
- No real patient data in fixtures, examples, or documentation.
- Use logical deactivation for core records to preserve appointment history.
- Authentication and staff authorization are deferred unless explicitly added to the MVP.

## Inspiration and adaptation

The referenced Docker examples were reviewed for general development patterns only. This project will keep the useful ideas—Compose-based startup, environment templates, an entrypoint, and repeatable migration commands—while using PostgreSQL and a domain-oriented Django structure. No repository code will be copied into this project.

## Open decision before implementation

The MVP still needs one product decision: whether all API endpoints are open for local development, or whether appointment and master-data endpoints require authenticated staff users from the beginning.

## AWS learning path

After the Docker Compose baseline is verified, this project will evolve through an AWS learning path. The first cloud deployment targets ECS/Fargate with RDS PostgreSQL, an Application Load Balancer, IAM roles, Secrets Manager, KMS, SQS, SNS, and CloudWatch. Kubernetes/EKS is a second-stage migration of the same containerized application, not a prerequisite for the first AWS deployment.

The AWS architecture and service-level specifications are indexed in [the AWS specification](2026-11-11-aws-end-to-end-design.md). The AWS work must preserve this document's domain boundaries, fictional-data constraint, and API contract.
