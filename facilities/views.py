from rest_framework import viewsets
from .models import Office
from .serializers import OfficeSerializer
class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by("name")
    serializer_class = OfficeSerializer
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])

