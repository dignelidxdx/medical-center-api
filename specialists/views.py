from rest_framework import viewsets
from .models import Specialty, Specialist
from .serializers import SpecialtySerializer, SpecialistSerializer
class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all().order_by("name")
    serializer_class = SpecialtySerializer
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Specialist.objects.select_related("specialty").all().order_by("last_name", "first_name")
    serializer_class = SpecialistSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        specialty = self.request.query_params.get("specialty")
        search = self.request.query_params.get("search")
        if specialty: qs = qs.filter(specialty_id=specialty)
        if search: qs = qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search)
        return qs
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])

