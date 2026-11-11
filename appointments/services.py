from django.core.exceptions import ValidationError
from django.db.models import Q
from scheduling.models import WorkingSchedule

def validate_appointment(instance):
    if instance.start_at >= instance.end_at: raise ValidationError("end_at must be after start_at")
    if instance.status != instance.Status.SCHEDULED: return
    for obj in (instance.specialist, instance.patient, instance.office):
        if not obj.is_active: raise ValidationError("All appointment participants must be active")
    weekday = instance.start_at.weekday()
    schedules = WorkingSchedule.objects.filter(specialist=instance.specialist, weekday=weekday, is_active=True)
    if not any(s.start_time <= instance.start_at.timetz().replace(tzinfo=None) and s.end_time >= instance.end_at.timetz().replace(tzinfo=None) for s in schedules):
        raise ValidationError("Appointment must fit within the specialist's working schedule")
    from .models import Appointment
    overlaps = Appointment.objects.filter(status=Appointment.Status.SCHEDULED, start_at__lt=instance.end_at, end_at__gt=instance.start_at).filter(Q(specialist=instance.specialist) | Q(office=instance.office)).exclude(pk=instance.pk)
    if overlaps.exists(): raise ValidationError("The specialist or office already has an overlapping appointment")

