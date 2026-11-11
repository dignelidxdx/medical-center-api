from django.core.exceptions import ValidationError
from django.db import models
from specialists.models import Specialist

class WorkingSchedule(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="working_schedules")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["specialist", "weekday", "start_time", "end_time"], name="unique_specialist_schedule")]
    def clean(self):
        if self.start_time >= self.end_time: raise ValidationError("end_time must be after start_time")

