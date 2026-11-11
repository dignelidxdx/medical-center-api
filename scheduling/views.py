from rest_framework import viewsets
from .models import WorkingSchedule
from .serializers import WorkingScheduleSerializer
class WorkingScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkingSchedule.objects.select_related("specialist").all().order_by("weekday", "start_time")
    serializer_class = WorkingScheduleSerializer
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])

