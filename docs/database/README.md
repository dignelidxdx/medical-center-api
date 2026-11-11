# Database Schema

Django migrations are the authoritative database schema for this project. PostgreSQL DDL is generated from those migrations and should not be edited manually as the primary migration mechanism.

Apply the schema with:

```bash
docker compose exec web python manage.py migrate
```

Inspect the SQL generated for an individual migration with:

```bash
docker compose exec web python manage.py sqlmigrate specialists 0001
```

The `schema.sql` file is a human-readable reference for the domain tables. If the models change, update migrations first and regenerate or review the reference DDL.

