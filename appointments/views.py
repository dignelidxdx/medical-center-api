from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("specialist", "patient", "office").all()
    serializer_class = AppointmentSerializer
    filterset_fields = ["specialist", "patient", "office", "status"]
    def perform_destroy(self, instance):
        instance.status = Appointment.Status.CANCELLED
        instance.save(update_fields=["status", "updated_at"])

