from django.db import models
from facilities.models import Office
from patients.models import Patient
from specialists.models import Specialist

class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
    specialist = models.ForeignKey(Specialist, on_delete=models.PROTECT, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="appointments")
    office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name="appointments")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    reason = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["start_at"]

