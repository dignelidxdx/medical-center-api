from datetime import date, datetime, time, timezone

import pytest
from rest_framework.test import APIClient

from facilities.models import Office
from patients.models import Patient
from specialists.models import Specialist, Specialty


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def base_records(db):
    specialty = Specialty.objects.create(name="Cardiology")
    specialist = Specialist.objects.create(first_name="Ada", last_name="Lovelace", license_number="LIC-1", email="ada@example.com", specialty=specialty)
    patient = Patient.objects.create(first_name="Grace", last_name="Hopper", document_number="DOC-1", date_of_birth=date(1980, 1, 1))
    office = Office.objects.create(name="Office 1")
    return specialty, specialist, patient, office


@pytest.mark.django_db
def test_master_data_can_be_created(client):
    response = client.post("/api/v1/specialties/", {"name": "Neurology"}, format="json")
    assert response.status_code == 201
    assert response.json()["name"] == "Neurology"


@pytest.mark.django_db
def test_appointment_requires_schedule_and_active_records(client, base_records):
    _, specialist, patient, office = base_records
    start = datetime(2026, 11, 16, 10, 0, tzinfo=timezone.utc)
    response = client.post("/api/v1/appointments/", {"specialist": specialist.id, "patient": patient.id, "office": office.id, "start_at": start.isoformat(), "end_at": datetime(2026, 11, 16, 11, 0, tzinfo=timezone.utc).isoformat()}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_back_to_back_appointments_are_allowed(client, base_records):
    from scheduling.models import WorkingSchedule
    _, specialist, patient, office = base_records
    WorkingSchedule.objects.create(specialist=specialist, weekday=0, start_time=time(9), end_time=time(12))
    payload = {"specialist": specialist.id, "patient": patient.id, "office": office.id, "start_at": "2026-11-16T09:00:00Z", "end_at": "2026-11-16T10:00:00Z"}
    assert client.post("/api/v1/appointments/", payload, format="json").status_code == 201
    payload.update(start_at="2026-11-16T10:00:00Z", end_at="2026-11-16T11:00:00Z")
    assert client.post("/api/v1/appointments/", payload, format="json").status_code == 201

